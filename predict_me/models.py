""" NOTE:
Modeling is very simple in our case we could fetch all data with two queries
which is why i revoked from creating model managers.
"""
from django.db import models
from django.contrib.postgres.fields import JSONField


class GoogleAdsData(models.Model):
    ad_clicks = models.PositiveIntegerField(default=0)
    account_id = models.PositiveIntegerField()
    adgroup_id = models.PositiveIntegerField()
    keyword_id = models.PositiveIntegerField()
    campaign_id = models.PositiveIntegerField()
    impressions = models.PositiveIntegerField()
    georgian_date = models.DateField()

    class Meta:
        managed = True
        db_table = "GoogleAdsData"  # Easier name when performing raw queries
        get_latest_by = "georgian_date"

    def __str__(self):
        """ This here is useless. """
        return f"Account Number {self.account_id}"


class WeatherData(models.Model):
    """ in my opinion it was not necessary to connect these two tables """
    weather_data = JSONField()
    georgian_date = models.DateField()

    class Meta:
        managed = True
        db_table = "WeatherData"  # Easier name when performing raw queries
        get_latest_by = "georgian_date"

    def __str__(self):
        return f"{self.georgian_date}"
