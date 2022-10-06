# pylint: disable=missing-module-docstring

from datetime import date
import sys
import requests

TODAY = str(date.today())

BASE_URI = "https://weather.lewagon.com"

GEO = "/geo/1.0/direct?"

FORECAST = "/data/2.5/forecast?"

# Handle error messages better

def search_city(query):
    '''Look for a given city. If multiple options are returned, have the user choose between them.
       Return one city (or None)
    '''
    query_url = BASE_URI + GEO

    params = dict(q=query.capitalize(), limit=5)

    response = requests.get(query_url, params=params).json()


    while len(response) == 0:

        print(f"Sorry, no place with the name '{query.title()}' could be found. Did you spell it correctly?\n")

        message = 'Please re-enter the name of the place correctly or enter another place name:\n> '

        query = input(message)

        params = dict(q=query.capitalize(), limit=5)

        response = requests.get(query_url, params=params).json()


    if len(response) > 1:

        print(f"There are several places with a name resembling '{query}':\n")

        for i in range(len(response)):

            print(f"{i+1}. {response[i]['name']} at {response[i]['lat']} and {response[i]['lon']}")

        print("\n")

        message = f'Which place did you mean? Type the number.\n> '

        choice = int(input(message))

        return response[choice-1]


    return response[0]


def weather_forecast(lat, lon):
    '''Return a 5-day weather forecast for the city, given its latitude and longitude.'''

    query_url = BASE_URI + FORECAST

    params = dict(lat=str(lat), lon=str(lon))

    response = requests.get(query_url, params=params).json()


    forecast = []


    for i in range(len(response["list"])):
        if response["list"][i]["dt_txt"].split()[0] == TODAY:

            continue

        if response["list"][i]["dt_txt"].split()[1] == "12:00:00":
            weather_description = str(response["list"][i]["weather"][0]["description"])
            weather_temp = str(round(response['list'][i]['main']['temp']-273.15, 1)) + "°"
            weather_date = str(response["list"][i]["dt_txt"].split()[0])
            weather = weather_date + ": " + weather_description.capitalize() + " " + weather_temp


            forecast.append({'weather': weather})

    print(forecast)
    return forecast


def main():
    '''Ask user for a city and display weather forecast'''
    query = input("City?\n> ")
    city = search_city(query)

    return weather_forecast(city['lat'], city['lon'])

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
