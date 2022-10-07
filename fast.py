
#from xmlrpc.client import DateTime
from fastapi import FastAPI #, APIRouter, BackgroundTasks
#import pandas as pd
#import pytz
#import datetime as dt

# from datetime import date
# import sys
# import requests
from flask import Flask, Response, request
import json

#app = FastAPI()

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
    res = {
        "fulfillment_response": {
            "messages": [
                {
                    "text": {
                        "text": [
                            req['sessionInfo']['parameters']['location']['original']#text
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
