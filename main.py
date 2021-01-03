# --- IMPORTS ---
import requests
import os
from twilio.rest import Client
# To use in python everywhere
# from twilio.http.http_client import TwilioHttpClient

# --- CONSTANTS ---
USER_LAT = -33.469551
USER_LNG = -70.704819
RAIN_LAT = 33.53
RAIN_LNG = -81.42
API_URL = "https://api.openweathermap.org/data/2.5/onecall"
API_KEY = os.environ.get("OWM_API_KEY")


# --- GLOBALS ---
params = {
    "lat": RAIN_LAT,
    "lon": RAIN_LNG,
    "appid": API_KEY,
    "exclude": "current,minutely,daily",
}


# --- FUNCTIONS ---
def main():
    response = requests.get(url=API_URL, params=params)
    response.raise_for_status()
    # print(response.status_code)
    hourly_data = response.json()["hourly"]

    # todo: create a list of the weather id for the next 12 hours and check if is raining
    #  Can switch to a current raining location found in ventusky.com
    weather_ids = [data["weather"][0]["id"] for data in hourly_data[:12]]
    # print(weather_ids)

    will_rain = False
    for code in weather_ids:
        if code < 700:
            will_rain = True

    if will_rain:
        # To use in python everywhere
        # proxy_client = TwilioHttpClient()
        # proxy_client.session.proxies = {'https': os.environ['https_proxy']}

        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        phone_number = os.environ.get("TWILIO_PHONE_NUMBER")
        receiver_number = os.environ.get("PHONE_NUMBER")
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body="It's going to rain today, bring an umbrella.",
            from_=phone_number,
            to=receiver_number
        )
        print(message.status)


# --- RUN ---
if __name__ == '__main__':
    main()
