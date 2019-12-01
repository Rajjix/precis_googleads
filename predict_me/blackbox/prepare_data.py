import csv
import copy
from django.conf import settings
from functools import lru_cache
from predict_me.models import GoogleAdsData, WeatherData

APP_NAME = 'predict_me'

required_data = [

    # Google Ads Data
    'ad_clicks',
    'impressions',

    'campaign_id',
    # Weather Data
    'dewPoint',
    'humidity',
    'windSpeed',
    'apparentTemperatureLow',
    'apparentTemperatureHigh'
]


def get_value(value):
    if '.' in str(value):
        try:
            return float(value)
        except Exception:
            return int(value)
    return int(value)


def prepare_train_data():
    """ Import data form our db and extract required info for training """

    # We create our training file with the correct header.
    # NOTE: if file exists it will be overwritten.
    TRAIN_DATA_PATH = f"{settings.BASE_DIR}/{APP_NAME}/blackbox/train_data.csv"
    train_data_f = open(TRAIN_DATA_PATH, 'w')
    csvwriter = csv.writer(train_data_f)
    csvwriter.writerow(required_data)

    # Get required data from db. (no need to evaluate queries into lists)
    historical_weather_data = copy.deepcopy(WeatherData.objects.all())
    google_ads_data = copy.deepcopy(GoogleAdsData.objects.all().values())

    @lru_cache()  # multiple objects use the same weather data
    def get_weather_data(date: str):
        return next(x.weather_data for x in historical_weather_data
                    if x.georgian_date == date)

    # We create a dictionary of each ad containing required data for training
    for ad in google_ads_data:
        ad.update(get_weather_data(ad["georgian_date"]))
        row = {k: get_value(v) for k, v in ad.items() if k in required_data}
        csvwriter.writerow([row[key] for key in required_data])
    train_data_f.close()  # None
    return TRAIN_DATA_PATH
