import os
import numpy as np
from predict_me.models import GoogleAdsData
from tensorflow.keras.models import load_model

MODEL_PATH = (f"{os.path.dirname(os.path.abspath(__file__))}"
              "/google_ads_model.h5")

# Required weather data we need to feed to our network for a
# PRECISE prediction 😊.
weather_input = ['dewPoint', 'humidity', 'windSpeed',
                 'apparentTemperatureLow', 'apparentTemperatureHigh']


def format_input(campaign_id, weather_data):
    # formats the required data to feed to our modal for prediction.
    return [campaign_id, *[weather_data.get(key, 0) for key in weather_input]]


def predict_data(account_id, date):
    """
    Tries to load the modal then for each input we predict number
    of impressions and clicks
    """

    # in case we don't have a model don't waste any more
    # computing power or db queries just throw.
    # probably here we can have a channel report bot or something.
    try:
        model = load_model(MODEL_PATH)
    except OSError:
        return {"hadError": True,
                "errorMessage": "Couldn't find prediction model"}

    campaigns = GoogleAdsData.objects.filter(
        account_id=account_id).distinct('campaign_id')

    def predict(campaign_id, weather_data):
        # we put data in an array to feed our network.
        info = format_input(campaign_id, weather_data)
        prediction = model.predict(np.array(info).reshape(1, -1))
        return int(prediction[0][0]), int(prediction[0][1])

    def predict_by_campaign(c_id, date):
        clicks, impressions = predict(c_id, date)
        prediction = {
            "campaign_id": c_id,
            "clicks": clicks,
            "impressions": impressions
        }
        return prediction

    results = [predict_by_campaign(x.campaign_id, date) for x in campaigns]

    prediction = {
        "hadError": False,
        "results": results
    }

    return prediction
