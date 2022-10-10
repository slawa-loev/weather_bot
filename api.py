
#from xmlrpc.client import DateTime
#from fastapi import FastAPI #, APIRouter, BackgroundTasks
#import pandas as pd
#import pytz
#import datetime as dt

# from datetime import date
# import sys
import requests
from flask import Flask, Response, request
import json
from datetime import datetime, timedelta
from weather_api.weather_request import process_request, search_location, weather_forecast
#from weather_api.params import BASE_URI, GEO, FORECAST


#app = FastAPI()

# BASE_URI = "https://weather.lewagon.com"

# GEO = "/geo/1.0/direct?"

# FORECAST = "/data/2.5/forecast?"

app = Flask(__name__)

# http://127.0.0.1:8000/predict?pickup_datetime=2012-10-06 12:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2

#@app.get("/") # fastapi interface
@app.route("/") # flask interface
def home():
    return {"Hello": "World"}

#@app.post("/my_webhook")
@app.route('/my_webhook', methods=['POST'])
def handle_webhook(): # request

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

    # tag = req["fulfillmentInfo"]["tag"]

    # loc_info = req['sessionInfo']['parameters']['location']
    # loc_keys = list(loc_info.keys())
    # loc_keys.remove('original') # remove the original key, to extract relevant key
    # location_query = loc_info[loc_keys[0]]

    #location = search_location(location_query)

    # search_location(location_query)

    query_info = process_request(req)

    message_date = query_info['date'].strftime("%A, %d %B %Y")
    time_verb = 'is expected to be' if query_info['date'] >= today else 'was'
    ## handling for invalid dates

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
        ambiguity_message = f"It looks like there are several places with names resembling '{query_info['location_name']}', so I went ahead and fetched information for {max_locations_per_name} of them:\n \n"

        temps = [weather_forecast(city_info[i]['lat'], city_info[i]['lon'], query_info['date']) for i in range(len(city_info))]

        city_descriptions = [f"""For {message_date}, in {query_info['location_name']}, {city_info[i]['admin1']} ({city_info[i]['country']}),
                             the minimum temperature {time_verb} {temps[i]['min_temp']}°C and the maximum temperature {temps[i]['max_temp']}°C\n""" for i in range(len(city_info))]

        message = ambiguity_message + "\n".join(city_descriptions)

        res['fulfillment_response']['messages'][0]['text']['text'][0] = message

        return Response(json.dumps(res), 200, mimetype='application/json')


    temps = weather_forecast(city_info[0]['lat'], city_info[0]['lon'], query_info['date'])

    message = f"""For {message_date}, in {query_info['location_name']} (in {query_info['admin1']}, {query_info['country']}),
    the minimum temperature {time_verb} {temps['min_temp']}°C and the maximum temperature {temps['max_temp']}°C"""

    res['fulfillment_response']['messages'][0]['text']['text'][0] = message


    return Response(json.dumps(res), 200, mimetype='application/json')


### Run a webhook on localhost
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)


# if $session.params.location.city != null
#   I gather that you want me to check the weather in $session.params.location.city on $sys.func.FORMAT_DATE($session.params.date, "EEEE, dd MMMM yyyy", "en"). Is this correct?
# elif $session.params.location.admin-area != null
#   I gather that you want me to check the weather in $session.params.location.admin-area on $sys.func.FORMAT_DATE($session.params.date, "EEEE, dd MMMM yyyy", "en"). Is this correct?
# elif $session.params.location.subadmin-area != null
#   I gather that you want me to check the weather in $session.params.location.admin-area on $sys.func.FORMAT_DATE($session.params.date, "EEEE, dd MMMM yyyy", "en"). Is this correct?
# elif $session.params.location.country != null
#   I gather that you want me to check the weather in $session.params.location.country on $sys.func.FORMAT_DATE($session.params.date, "EEEE, dd MMMM yyyy", "en"). Is this correct?
# elif $session.params.location.island != null
#   I gather that you want me to check the weather on $session.params.location.island on $sys.func.FORMAT_DATE($session.params.date, "EEEE, dd MMMM yyyy", "en"). Is this correct?
# elif $session.params.location.business-name != null
#   I gather that you want me to check the weather in $session.params.location.business-name at $sys.func.FORMAT_DATE($session.params.date, "EEEE, dd MMMM yyyy", "en"). Is this correct?
# elif $session.params.location.street-address != null
#   I gather that you want me to check the weather at $session.params.location.street-address on $sys.func.FORMAT_DATE($session.params.date, "EEEE, dd MMMM yyyy", "en"). Is this correct?
# elif $session.params.location.zip-code != null
#   I gather that you want me to check the weather at $session.params.location.zip-code on $sys.func.FORMAT_DATE($session.params.date, "EEEE, dd MMMM yyyy", "en"). Is this correct?
# elif $session.params.location.shortcut != null
#   I gather that you want me to check the weather at $session.params.location.shortcut on $sys.func.FORMAT_DATE($session.params.date, "EEEE, dd MMMM yyyy", "en"). Is this correct?
# else
#   I gather that you want me to check the weather in $session.params.location on $sys.func.FORMAT_DATE($session.params.date, "EEEE, dd MMMM yyyy", "en"). Is this correct?
# endif
