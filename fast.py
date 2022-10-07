
#from xmlrpc.client import DateTime
from fastapi import FastAPI, APIRouter, BackgroundTasks
#import pandas as pd
#import pytz
#import datetime as dt

# from datetime import date
# import sys
# import requests
from flask import request
import json

from matplotlib.font_manager import json_load

app = FastAPI()


APIRouter

# http://127.0.0.1:8000/predict?pickup_datetime=2012-10-06 12:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2
@app.post("/")
#@app.get("/")
def handle_webhook(): # request

    req = request.get_json()

    tag = req["fulfillmentInfo"]["tag"]

    if tag == "Default Welcome Intent":
        text = "Hello from a GCF Webhook"
    elif tag == "get-name":
        text = "My name is Flowhook"
    else:
        text = f"There are no fulfillment responses defined for {tag} tag"

    # You can also use the google.cloud.dialogflowcx_v3.types.WebhookRequest protos instead of manually writing the json object
    # Please see https://googleapis.dev/python/dialogflow/latest/dialogflow_v2/types.html?highlight=webhookresponse#google.cloud.dialogflow_v2.types.WebhookResponse for an overview
    res = {
        "fulfillment_response": {
            "messages": [
                {
                    "text": {
                        "text": [
                            text
                        ]
                    }
                }
            ]
        }
    }

    # Returns json
    return res


# def root():
#     return {'greeting': 'Hello'}

# @app.get("/predict")
# def predict(pickup_datetime, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count):

#     utc = pytz.utc
#     time_loc = utc.localize(pd.to_datetime(pickup_datetime))
#     fmt="%Y-%m-%d %H:%M:%S UTC"
#     time_utc=time_loc.strftime(fmt)


#     dt.datetime.strptime(pickup_datetime, '%Y-%m-%d %H:%M:%S')

#     X_pred = pd.DataFrame(dict(key=[time_utc],
#                                pickup_datetime=[time_utc], # format="%Y-%m-%d %H:%M:%S UTC"
#                                pickup_longitude=float(pickup_longitude),
#                                pickup_latitude=float(pickup_latitude),
#                                dropoff_longitude=float(dropoff_longitude),
#                                dropoff_latitude=float(dropoff_latitude),
#                                passenger_count=int(passenger_count)
#                                 ))


#     return {"fare_amount" : float(pred(X_pred)[0])}
#     #return {"fare_amount" : float(app.state.model.predict(X_pred)[0])}
