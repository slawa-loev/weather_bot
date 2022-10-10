
#import requests
from flask import Flask, Response, request
import json
from datetime import datetime, timedelta
from weather_api.weather_request import process_request, search_location, weather_forecast


app = Flask(__name__)

@app.route("/") # flask interface
def home():
    return {"Hello": "World"}

@app.route('/get_weather', methods=['POST'])
def get_weather():

    today = datetime.today().date()
    message=""
    res = {
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


    req = request.get_json()

    query_info = process_request(req)

    message_date = query_info['date'].strftime("%A, %d %B %Y")
    time_verb = 'is expected to be' if query_info['date'] >= today else 'was'

    ## handling invalid dates

    if query_info['date'] > today + timedelta(days=7):
        res['fulfillment_response']['messages'][0]['text']['text'][0] = f"Sorry, {message_date}, is too far in the future."
        return Response(json.dumps(res), 200, mimetype='application/json')

    if query_info['date'] < today and not query_info['date'] < today - timedelta(days=7):
        res['fulfillment_response']['messages'][0]['text']['text'][0] = f"Sorry, {message_date}, is too recent for my records."
        return Response(json.dumps(res), 200, mimetype='application/json')

    max_locations_per_name=3

    city_info = search_location(query_info['location_name'], max_locations_per_name)

    ## handling for invalid or ambigious location names

    if city_info == None:
        res['fulfillment_response']['messages'][0]['text']['text'][0] = f"Sorry, I could not find a location with the name '{query_info['location_name']}'."
        return Response(json.dumps(res), 200, mimetype='application/json')

    if len(city_info) > 1:
        ambiguity_message = f"It looks like there are several places with the name '{query_info['location_name']}', so I went ahead and fetched information for {max_locations_per_name} of them:\n \n"

        temps = [weather_forecast(city_info[i]['lat'], city_info[i]['lon'], query_info['date']) for i in range(len(city_info))]

        city_descriptions = [f"""For {message_date}, in {query_info['location_name']}, {city_info[i]['admin1']} ({city_info[i]['country']}),
                             the temperature {time_verb} between {temps[i]['min_temp']}°C and {temps[i]['max_temp']}°C.\n""" for i in range(len(city_info))]

        message = ambiguity_message + "\n".join(city_descriptions)

        res['fulfillment_response']['messages'][0]['text']['text'][0] = message

        return Response(json.dumps(res), 200, mimetype='application/json')


    temps = weather_forecast(city_info[0]['lat'], city_info[0]['lon'], query_info['date'])

    message = f"""For {message_date}, in {query_info['location_name']} (in {query_info['admin1']}, {query_info['country']}),
    the temperature {time_verb} between {temps['min_temp']}°C and temperature {temps['max_temp']}°C."""

    res['fulfillment_response']['messages'][0]['text']['text'][0] = message

    return Response(json.dumps(res), 200, mimetype='application/json')


### Run a webhook on localhost
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
