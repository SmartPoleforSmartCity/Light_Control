import RPi.GPIO as GPIO
from datetime import datetime as date
from time import sleep as delay
import requests

light_pin = 20

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(light_pin, GPIO.OUT)
GPIO.output(light_pin,0)

#สั่งปิดไฟด้วยสัญญาณไฟ 
try:
    while True:
        result = requests.get("http://34.143.237.67:8000/pole_light")
        time_now = date.now().strftime("%H:%M:%S")
        if time_now >= "18:00:00":
            GPIO.output(light_pin,0)
        elif time_now >= "06:00:00":
            GPIO.output(light_pin,1)
        if result.json() == 0 and date.now().strftime("%H:%M:%S") > "18:00:00" :
            GPIO.output(light_pin,1)
            count = 0
            while count < 1800:
                count += 1
                delay(1)
            GPIO.output(light_pin,1)
            info = {"status": 1}
            requests.post("http://34.143.237.67:8000/pole_light",data=info)
        else:
            GPIO.output(light_pin,result.json())
        delay(10)
except Exception as e:
    print(e)
