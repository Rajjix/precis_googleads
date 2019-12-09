import csv
import asyncio
from datetime import datetime as dt
from itertools import islice
from .models import GoogleAdsData, WeatherData
from .helpers import parse_date
from .dark_sky import fetch_weather_data


def populate_database_with_weather_data(weather_data: dict):
    if len(weather_data):
        weather_objects = (WeatherData(
            georgian_date=key,
            weather_data=value
        ) for key, value in weather_data.items())
        WeatherData.objects.bulk_create(weather_objects, len(weather_data))


async def get_weather_forecasts(list_of_dates, length):
    # Chooses max number of threads on machine by default.
    futures = [
        asyncio.get_event_loop().run_in_executor(
            None,
            fetch_weather_data,
            next(list_of_dates)
        ) for i in range(length)
    ]
    return {date: response for date, response in await asyncio.gather(*futures)}  # nopep8


def populate_db_with_csv_data(path):

    with open(path) as csv_file:
        data = csv.DictReader(csv_file)
        ads_data = [x for i, x in enumerate(data)]

    # Process date information gathering. we try not to recreate old data.

    existing_dates = set(dt.strftime(x.georgian_date, "%Y-%m-%d")
                         for x in WeatherData.objects.all())

    weather_dates = set(x["day"]
                        for x in ads_data if parse_date(x["day"]))

    weather_dates = weather_dates - existing_dates

    # machine gun mode active. try to run as many requests simultanuosly.
    # with aiohttp this would be even faster.
    # Currently we're limited by the number of threads we own.
    weather_data = asyncio.run(
        get_weather_forecasts(
            iter(weather_dates), len(weather_dates)))
    populate_database_with_weather_data(weather_data)

    # Unless the data gets big enough or we add some kind of unique identifier
    # for ads details we can delete them and recreate.
    # if new data has key errors old data would not be deleted. stay safe!.
    ad_objects = (GoogleAdsData(
        ad_clicks=obj["clicks"],
        georgian_date=obj["day"],
        account_id=obj["accountId"],
        adgroup_id=obj["adgroupId"],
        keyword_id=obj["keywordId"],
        campaign_id=obj["campaignId"],
        impressions=obj["impressions"],
    ) for obj in ads_data)

    GoogleAdsData.objects.all().delete()

    # just in case we have a huge amount of data
    batch_size = 10000
    while True:
        batch = list(islice(ad_objects, batch_size))
        if not batch:
            break
        GoogleAdsData.objects.bulk_create(batch, batch_size)
    # GoogleAdsData.objects.bulk_create(ad_objects, len(ads_data))
