from typing import Iterable, Union
from django.http import JsonResponse
from datetime import date, datetime as dt, timedelta


def parse_params(items: Iterable, *args: tuple) -> tuple:
    """ args is a tuple of required query params """
    query_params = dict(items)
    return (query_params.get(x) for x in args)


def error_response(msg: str):
    """ Make life simeple with a simple message """
    return JsonResponse({"hadError": True,
                         "errorMessage": msg})


def parse_date(date_str: str) -> Union[bool, str]:
    """ date must be of format yyyy-mm-dd """
    try:
        return dt.strftime(dt.strptime(date_str, '%Y-%m-%d').date(),
                           '%Y-%m-%d')
    except (TypeError, ValueError):
        return False


def valid_date_timespan(date_str: str) -> bool:
    """ returns true if date in 7 days time span else false """
    return (date.today() <= dt.strptime(date_str, '%Y-%m-%d').date()
            <= date.today() + timedelta(days=7))
