
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
from datetime import datetime
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

    req = request.get_json()

    # tag = req["fulfillmentInfo"]["tag"]

    # loc_info = req['sessionInfo']['parameters']['location']
    # loc_keys = list(loc_info.keys())
    # loc_keys.remove('original') # remove the original key, to extract relevant key
    # location_query = loc_info[loc_keys[0]]

    #location = search_location(location_query)

    # search_location(location_query)

    query_info = process_request(req)

    coords = search_location(query_info['location_name'])

    temps = weather_forecast(coords['lat'], coords['lon'], query_info['date'])

    message_date = query_info['date'].strftime("%A, %d %B %Y")

    message = f"""For {message_date}, in {query_info['location_name']}, the minimum temperature is expected to be {temps['min_temp']}°C and the maximum temperature {temps['max_temp']}°C"""

    #req['sessionInfo']['parameters']['date']

    # parameters = []
    # for key, value in req['sessionInfo']['parameters'].items():
    #      parameters.append({'name':key,'value':value})

    # if tag == "Default Welcome Intent":
    #     text = "Hello from a GCF Webhook"
    # elif tag == "get-name":
    #     text = "My name is Flowhook"
    # else:
    #     text = f"There are no fulfillment responses defined for {tag} tag"

    # You can also use the google.cloud.dialogflowcx_v3.types.WebhookRequest protos instead of manually writing the json object
    # Please see https://googleapis.dev/python/dialogflow/latest/dialogflow_v2/types.html?highlight=webhookresponse#google.cloud.dialogflow_v2.types.WebhookResponse for an overview

    #{'date': {'year': 2022.0, 'month': 10.0, 'day': 10.0}, 'location': {'city': 'New York', 'original': 'ny'}}

    res = {
        "fulfillment_response": {
            "messages": [
                {
                    "text": {
                        "text": [


                            #f"{req['sessionInfo']['parameters']['location'][location_query]}"
                            #search_location(location_query)
                            message
                            #req['sessionInfo']['parameters']['location']['original']#text
                            #req['session_info']['parameters']['location']['original']#text
                        ]
                    }
                }
            ]
        }
    }

    # Returns json
    return Response(json.dumps(res), 200, mimetype='application/json')
    #return res

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
