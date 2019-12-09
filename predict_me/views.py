from django.http import JsonResponse
from django.core.cache import cache
from .models import GoogleAdsData
from .blackbox import predict_data
from .dark_sky import fetch_weather_data
from functools import lru_cache
from .helpers import (
    error_response as err_resp, parse_date, parse_params,
    valid_date_timespan)


@lru_cache()
def get_account_id(account_id):
    if account_id.isdigit():
        return GoogleAdsData.objects.filter(account_id=account_id).count()
    return None


def call_me_oracle(request):
    account_id, date = parse_params(request.GET.items(), "account_id", "date")

    # account_id and a valid date format are mandatory.
    if (not account_id or not parse_date(date)):
        return err_resp("account_id<int> and date<yyyy-mm-dd> are required")

    # date must be withint a week from today.
    if not valid_date_timespan(date):
        return err_resp("date must be within a week from today")

    if not get_account_id(account_id):
        return err_resp("Account not found")

    # update cache with date if necessary.
    if not cache.get(date):
        weather_data = fetch_weather_data(date)
        cache.set(date, weather_data, 600)

    weather_data = cache.get(date)
    # perform some magic.
    prediction = predict_data(account_id, weather_data[1])
    return JsonResponse(prediction)
