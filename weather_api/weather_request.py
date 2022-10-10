# pylint: disable=missing-module-docstring

from datetime import datetime
import requests


def process_request(request):
    '''extract location name and date from request
    '''

    loc_info = request['sessionInfo']['parameters']['location'] # access location info in request
    loc_keys = list(loc_info.keys()) # list location keys in request
    loc_keys.remove('original') # remove the original key (e.g. "ny" or "rottrdam"), to extract relevant key resolved by dialogflow (e.g. "New York" or "Rotterdam")
    location_query = loc_info[loc_keys[0]] # get the location name at relevant key # note, sometimes there will be more than one relevant key, e.g. if there is location: city: Amsterdam, admin:North Holland


    date_raw = request['sessionInfo']['parameters']['date']

    date_string = f"{int(date_raw['year'])}-{int(date_raw['month'])}-{int(date_raw['day'])}"

    date_object = datetime.strptime(date_string, "%Y-%m-%d").date()

    return {"location_name": location_query,
            "date": date_object}

def search_location(location_name, max_locations_per_name=3):
    '''Look for a given location. If none are returned, return None.
    If multiple are returned, return info for max_locations_per_name of them
    '''

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = dict(name=location_name.capitalize(), count=max_locations_per_name)

    response = requests.get(geo_url, params=geo_params).json()

    if response.get('results', None) == None:
        return None

    if len(response['results']) > 1:

        return [{"lat": response['results'][i]['latitude'],
          "lon": response['results'][i]['longitude'],
          "admin1": response['results'][i].get('admin1', ""),
          "country": response['results'][i].get('country', "")} for i in range(len(response['results']))]

    location_info = [{"lat": response['results'][0]['latitude'],
              "lon": response['results'][0]['longitude'],
              "admin1": response['results'][0].get('admin1', ""),
              "country": response['results'][0].get('country', "")}]


    return location_info


def weather_forecast(lat, lon, date):
    '''Return max and min temperature for a location/locations, given latitude and longitude.'''

    today = datetime.today().date()

    url = "https://api.open-meteo.com/v1/forecast?" if date >= today else "https://archive-api.open-meteo.com/v1/era5?" # check whether requested date is in the past or future, use corresponding url
    # for historical data there is the constraint that data is updated with a delay of 5-7 days.

    date_string = date.strftime("%Y-%m-%d")

    # daily weather variables need to be appended manually to url as the comma is not parsed when constructing the URL as accepted by the API

    daily_vars = 'temperature_2m_max,temperature_2m_min'

    daily = f'daily={daily_vars}'
    url = url + daily
    params = dict(
        latitude=lat,
        longitude=lon,
        timezone='auto',
        start_date=date_string,
        end_date=date_string)

    response = requests.get(url, params=params).json()

    max_temp = response['daily']['temperature_2m_max'][0]
    min_temp = response['daily']['temperature_2m_min'][0]


    return {"max_temp": max_temp,
            "min_temp": min_temp}
