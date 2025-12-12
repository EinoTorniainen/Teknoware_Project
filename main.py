import requests
import network
from machine import Pin,PWM
import time

pwm = PWM(Pin(27))
pwm.freq(1000)

# connect to wlan
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("name", "password")

while True:    
    # current time (seconds since 00:00)
    url = "https://timeapi.io/api/time/current/zone?timeZone=Europe%2FHelsinki"
    response = requests.get(url)
    data = response.json()
    currentHour = data["hour"]
    currentMinute = data["minute"]
    now_sec = (currentHour*60+currentMinute)*60

    #  get time of sunrise and sunset from api
    url = "https://api.sunrise-sunset.org/json?lat=60&lng=25&date=today&formatted=0&tzid=Europe/Helsinki"
    response = requests.get(url)
    data = response.json()
    sunrise = data["results"]["sunrise"]
    sunset = data["results"]["sunset"]

    # time of sunrise in seconds since 00:00
    srhr = int(sunrise[11:13])
    srmin = int(sunrise[14:16])
    srsec = (srhr*60+srmin)*60

    # time of sunset in seconds since 00:00
    sshr = int(sunset[11:13])
    ssmin = int(sunset[14:16])
    sssec = (sshr*60+ssmin)*60

    # turn light on/off based on time
    if now_sec > srsec and now_sec < sssec:
        pwm.duty_u16(40000)
    else:
        pwm.duty_u16(50000)
        
    time.sleep(300)