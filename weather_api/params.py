"""
api params
load and validate the environment variables in the `.env`
"""
import os

BASE_URI = os.environ.get("BASE_URI")
GEO = os.environ.get("GEO")
FORECAST = os.environ.get("FORECAST")