import time

import RPi.GPIO as GPIO

relay=17

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)
GPIO.output(relay, GPIO.HIGH)

time.sleep(2)

GPIO.output(relay, GPIO.LOW)
GPIO.cleanup()