import time
# from .models import GoogleAdsData, WeatherData


def predict_data(account_id, date):
    print("making some prediction...")
    print("=========================")
    time.sleep(2)
    print("Hold on, almost there!")
    print("=========================")
    time.sleep(3)
    print(f"Ok you're gonna have outstanging impressions on {date}")
    print("=========================")
    prediction = {"hadError": False,
                  "success_rate": "99%"}
    return prediction
