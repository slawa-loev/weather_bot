# pylint: disable=missing-module-docstring

from datetime import date
import sys
import requests
#from params import BASE_URI, GEO, FORECAST

#def init_info():

TODAY = str(date.today())

# BASE_URI = "https://weather.lewagon.com"

# GEO = "/geo/1.0/direct?"

# FORECAST = "/data/2.5/forecast?"


#https://weather.lewagon.com/geo/1.0/direct?q=Barcelona

def process_request(request):

    loc_info = request['sessionInfo']['parameters']['location'] # access location info in request
    loc_keys = list(loc_info.keys()) # list location keys in request
    loc_keys.remove('original') # remove the original key (e.g. "ny" or "rottrdam"), to extract relevant key resolved by dialogflow (e.g. "New York" or "Rotterdam")
    location_query = loc_info[loc_keys[0]] # get the location name at relevant key

    #location = search_location(location_query) # get coordinate of location name from weater api

    date = request['sessionInfo']['parameters']['date']

    return location_query, date

def search_location(query):
    '''Look for a given location. If multiple options are returned, have the user choose between them.
       Return one city (or None)
    '''

    # BASE_URI = "https://weather.lewagon.com"

    # GEO = "/geo/1.0/direct?"

    # query_url = BASE_URI + GEO

    # params = dict(q=query.capitalize(), limit=1)

    # response = requests.get(query_url, params=params).json()


    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = dict(name=query.capitalize(), count=1)

    response = requests.get(geo_url, params=geo_params).json()
    lat = response['results'][0]['latitude']
    lon = response['results'][0]['longitude']

    # if len(response) == 0:

    #     print(f"Sorry, no place with the name '{query.title()}' could be found. Did you spell it correctly?\n")

    #     message = 'Please re-enter the name of the place correctly or enter another place name:\n> '

    #     query = input(message)

    #     params = dict(q=query.capitalize(), limit=5)

    #     response = requests.get(query_url, params=params).json()


    # if len(response) > 1:

    #     print(f"There are several places with a name resembling '{query}':\n")

    #     for i in range(len(response)):

    #         print(f"{i+1}. {response[i]['name']} at {response[i]['lat']} and {response[i]['lon']}")

    #     print("\n")

    #     message = f'Which place did you mean? Type the number.\n> '

    #     choice = int(input(message))

    #     return response[choice-1]


    #return response[0]['name']
    #return response[0]
    return lat, lon


def weather_forecast(lat, lon):
    '''Return a 5-day weather forecast for the city, given its latitude and longitude.'''

    forecast_url = "https://api.open-meteo.com/v1/forecast?"
    # daily weather variables need to be appended manually to url as the comma is not parsed when constructing the URL as accepted by the API

    daily_vars = 'temperature_2m_max,temperature_2m_min'

    daily = f'daily={daily_vars}'
    forecast_url = forecast_url + daily
    date = '2022-10-12'
    forecast_params = dict(
        latitude=lat,
        longitude=lon,
        timezone='auto',
        start_date=date,
        end_date=date)

    response = requests.get(forecast_url, params=forecast_params).json()

    return response

def main():
    '''Ask user for a city and display weather forecast'''
    query = input("City?\n> ")
    city = search_location(query)

    return weather_forecast(city['lat'], city['lon'])

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
