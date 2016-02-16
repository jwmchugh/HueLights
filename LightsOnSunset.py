import json
import time
import datetime
import requests

LONGTITUDE="-6.652068"
LATITUDE="53.236967"
HUE_IP="http://192.168.1.4"
HUE_USER="/api/329a699810745e7f145c348107aae8f/"
MINS_BEFORE_SUNSET=45 # Number of minutes before sunset the lights should be turned on

def activation_time():
    # make web call
    r = requests.get("http://api.sunrise-sunset.org/json?lat="+LATITUDE + "&lng="+LONGTITUDE+"&date=today&formatted=0")
    json_response = r.json()
    long_sunsettime = (json_response["results"]["sunset"])
    sunset = datetime.datetime.strptime(long_sunsettime[0:19], "%Y-%m-%dT%H:%M:%S")
    sunset = sunset - datetime.timedelta(minutes=MINS_BEFORE_SUNSET)
    return sunset # minus the earlier time

def sleep_till_scheduled_time(lights_on_time):
    now = datetime.datetime.today()
    if lights_on_time < now:
        lights_on_time += datetime.timedelta(days=1)
    print ("Lights on time: " + str(lights_on_time))
    time.sleep((lights_on_time - now).seconds-(MINS_BEFORE_SUNSET * 60))

def activate_hue_lights():
    payload = {"on": True}
    r = requests.put("http://192.168.1.4/api/329a699810745e7f145c348107aae8f/groups/AllLights/action",json=payload)

while(True):
    sleep_till_scheduled_time(activation_time())
    activate_hue_lights()