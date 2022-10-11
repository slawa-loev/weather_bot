
import requests
from flask import Flask, Response, request
import json
from datetime import datetime, timedelta
from weather_api.weather_request import process_request, search_location, weather_forecast

app = Flask(__name__) # settingg up flask api object

@app.route('/get_weather', methods=['POST'])
def get_weather():

    today = datetime.today().date() ## getting today's date for later comparisons

    message="" ## setting an empty dummy message for api response

    res = { # setting up a properly formatted api response structure
        "fulfillment_response": {
            "messages": [
                {
                    "text": {
                        "text": [
                            message
                        ]
                    }
                }
            ]
        }
    }


    req = request.get_json() # getting the request json

    tag = req["fulfillmentInfo"]["tag"] # extracting tag

    if tag == "get_joke": # if tag comes from joke flow, we return a joke

        joke = requests.get('https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single').json()["joke"]
        res['fulfillment_response']['messages'][0]['text']['text'][0] = joke
        return Response(json.dumps(res), 200, mimetype='application/json')

    query_info = process_request(req) # if it is not from the joke flow, the request is processed to extract location name and date

    message_date = query_info['date'].strftime("%A, %d %B %Y") # creating a date string to be used in responses
    time_verb = 'is expected to be' if query_info['date'] >= today else 'was' # setting proper grammatical verb form depending on the date requested

    ## handling invalid dates

    if query_info['date'] > today + timedelta(days=7): # handles dates that are too far in the future
        res['fulfillment_response']['messages'][0]['text']['text'][0] = f"Sorry, {message_date}, is too far in the future."
        return Response(json.dumps(res), 200, mimetype='application/json')

    if query_info['date'] < today and not query_info['date'] < today - timedelta(days=7): # handles dates that are not far enough in the past
        res['fulfillment_response']['messages'][0]['text']['text'][0] = f"Sorry, {message_date}, is too recent for my records."
        return Response(json.dumps(res), 200, mimetype='application/json')

    max_locations_per_name=3 # sets a parameter for how many cities with the same name to get from the geo weather api

    location_info = search_location(query_info['location_name'], max_locations_per_name) # getting location info based on the name

    ## handling for invalid or ambigious location names

    if location_info == None: # handles requests for which the location name was not found
        res['fulfillment_response']['messages'][0]['text']['text'][0] = f"Sorry, I could not find a location with the name '{query_info['location_name']}'."
        return Response(json.dumps(res), 200, mimetype='application/json')

    if len(location_info) > 1: # handles requests for multiple location with the same name
        ambiguity_message = f"It looks like there are several places with the name '{query_info['location_name']}', so I went ahead and fetched information for {max_locations_per_name} of them:\n \n"

        temps = [weather_forecast(location_info[loc]['lat'], location_info[loc]['lon'], query_info['date']) for loc in range(len(location_info))]

        city_descriptions = [f"""For {message_date}, in {query_info['location_name']}{f" ({location_info[loc]['admin1']}, {location_info[loc]['country']}), " if location_info[loc]['admin1'] != "" else ", "}the temperature {time_verb} between {temps[loc]['min_temp']}°C and {temps[loc]['max_temp']}°C.\n""" for loc in range(len(location_info))]

        message = ambiguity_message + "\n".join(city_descriptions)

        res['fulfillment_response']['messages'][0]['text']['text'][0] = message

        return Response(json.dumps(res), 200, mimetype='application/json')

    # handles requests for exactly one location with the name

    temps = weather_forecast(location_info[0]['lat'], location_info[0]['lon'], query_info['date'])

    message = f"""For {message_date}, in {query_info['location_name']}{f" ({location_info[0]['admin1']}, {location_info[0]['country']}), " if location_info[0]['admin1'] != "" else ", "}the temperature {time_verb} between {temps['min_temp']}°C and temperature {temps['max_temp']}°C."""

    res['fulfillment_response']['messages'][0]['text']['text'][0] = message

    return Response(json.dumps(res), 200, mimetype='application/json')


### Run a webhook on localhost
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
