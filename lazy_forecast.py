#
# API provider used: https://www.weatherbit.io
# SMS sender used: https://www.twilio.com
# To run daily, you can host it on https://www.pythonanywhere.com
#
# Check the weather forecast for the next 12 hours. Gather precipitation data and
# temperature. And send you a SMS to tell you if you have to take your raincoat or not today ! :)
#

import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

WEATHERBIT_KEY = "your_weatherbit_api_key"
FORECAST_URL = "https://api.weatherbit.io/v2.0/forecast/hourly"

TWILIO_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE_NUMBER = "+xxxxxxxx your twilio phone number"
PHONE_NUMBER = "+xxxxxxxxxx your actual phone number"

# set up parameter to call weatherbit API. This will fetch weather forcast
# for the next 12 hours.
# City could be set also using zip code: "zip":"34000,fr"
params = {"key":WEATHERBIT_KEY,
          "units":"M",
          "hours":12,
          "city":"Montpellier,fr"} 

# Make a call to weatherbit and parse result
r = requests.get(FORECAST_URL, params=params)
if r.ok:
    json_result = r.json()

    temp = [t["temp"] for t in json_result["data"]]
    precipitation = [t["precip"] for t in json_result["data"]]
    max_precip = max(precipitation)
    min_temp = min(temp)
    max_temp = max(temp)

    # creating a body of the sms wich will be sent
    raincoat_msg = "Take your raincoat ! "
    if max_precip < 0.01:
        raincoat_msg = "You don't need your raincoat today :) ! "

    msg = (f"{raincoat_msg}"
           f"For the next 12 hours precipitation max: {max_precip:.4f}mm. "
           f"Min and max temperature: {min_temp}/{max_temp}°C")

    # connect to twilio and create ( send ) the sms.
    # we need to create a proxy client to be able to tell httplib2 ( used by
    # twilio ) which proxy settings to use;
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': "proxy.server:3128"}

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN, http_client=proxy_client)
    message = client.messages.create(
                            from_=TWILIO_PHONE_NUMBER,
                            body=msg,
                            to=PHONE_NUMBER
    )

    print("Message sent !")