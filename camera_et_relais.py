from picamera import PiCamera
from time import sleep
from time import time 
from os import system
import RPi.GPIO as GPIO

camera = PiCamera()
camera.resolution = (720,640)

relay=17
temps_entre_photo_voulu = 60
temps_relais=2
temps_calcul= temps_entre_photo_voulu-(2*temps_relais)
photos_par_gif = 60
sleep (10)
print("start")

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)
GPIO.setwarnings(False)

while 1: 
    
    GPIO.output(relay, GPIO.LOW)
    sleep(temps_relais)
    camera.capture('/media/julien/USBKEY/images/image%s.jpg' % int(time()))# indiquer image+date
    sleep(temps_relais)
    GPIO.output(relay, GPIO.HIGH)
    sleep(temps_entre_photo_voulu)

    #GPIO.cleanup()
    system('convert -delay 0.2 -loop 0 /media/julien/USBKEY/images/image*.jpg /media/julien/USBKEY/animation.gif')
    #sleep(5)
#system('chromium-browser animation.gif')
print("over")
