import requests
from datetime import datetime as dt

SECRET = '65bd03656e91f758b97e30aaecafb052'
DARK_SKY_API = 'https://api.darksky.net/forecast'

# [Sweden]
latitude = "59.3293"
longitude = "18.0686"

# [Curacao] # pretty hot there.
# latitude = "12.169"
# longitude = "68.9900"

# [Kharkiv]
# latitude = "49.9935"
# longitude = "36.2304"

# icon = ['clear-day', 'clear-night', 'rain', 'snow', 'sleet', 'wind',
#         'fog', 'cloudy', 'partly-cloudy-day', 'partly-cloudy-nigh']


def parse_datetime(date_str: str) -> str:
    """ parses date string to give us a valid time object for dark sky api """
    return dt.strftime(dt.strptime(date_str, '%Y-%m-%d'), "%Y-%m-%dT%H:%M:%S")


def weather_api_request(url, secret, date):
    """ returns a ready to use request function with provided date """
    req_url = (f"{url}/{secret}/{latitude},{longitude},{parse_datetime(date)}?"
               "exclude=currently,minutely,hourly,alerts,flags"
               "&units=auto&lang=en")
    return requests.get(req_url).json()


def fetch_weather_data(date: str):
    """ just in case we run out of api calls or dark sky gets hacked """
    try:
        w_data = weather_api_request(DARK_SKY_API, SECRET, date)
        return date, w_data["daily"]["data"][0]
    except Exception:  # report exception somewhere.
        return None
