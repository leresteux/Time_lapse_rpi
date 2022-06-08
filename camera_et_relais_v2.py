from picamera import PiCamera
from time import sleep
from time import time 
from os import system
import RPi.GPIO as GPIO
import os

camera = PiCamera()
camera.resolution = (720,640)

#variables
temps_entre_photo_voulu = 3 # > 2sec (contraint de 'temps_relais') 
photos_par_dossier = 2 # >100 si creation de gif sinon ca rame et encore faut teser
creation_gif = True 

#constante
relay=17
temps_relais=1
temps_calcul= temps_entre_photo_voulu-(2*temps_relais)
photos_prises=0
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)
GPIO.setwarnings(False)
nom_dossier=int(time())
nom_sous_dossier=0

#info console
print("Temps entre prise photos :", temps_entre_photo_voulu,"sec")
print("Mode creation GIF : ", creation_gif)
print("Nbre de photos par dossier :", photos_par_dossier)
print("Lancement dans 10 sec")

sleep (10)#le temps de le MEDIA soit monté si programme au démarrage

os.makedirs('/media/julien/USBKEY/capture_%s' % nom_dossier)

print("La boucle demarre")

while 1:
    if photos_prises == 0 :
        nom_sous_dossier += 1
        os.makedirs('/media/julien/USBKEY/capture_%s/%d' %(nom_dossier, nom_sous_dossier))
        print("creation d'un sous_dossier n°", nom_sous_dossier)
        sleep(1)
    if photos_prises < photos_par_dossier :
        GPIO.output(relay, GPIO.LOW)
        sleep(temps_relais)
        camera.capture('/media/julien/USBKEY/capture_%s/%d/image%s.jpg' %(nom_dossier, nom_sous_dossier,int(time())))# indiquer image+date
        sleep(temps_relais)
        GPIO.output(relay, GPIO.HIGH)
        photos_prises += 1
        sleep(temps_entre_photo_voulu)
        print("photo prise n°", photos_prises,"/", photos_par_dossier," avant crea GIF")
    else:
        photos_prises=0
        print("mode creation GIF : ", creation_gif)
        if creation_gif :
            system('convert -delay 0.2 -loop 0 /media/julien/USBKEY/capture_%s/%d/image*.jpg /media/julien/USBKEY/capture_%s/%d/animation%d.gif' %(nom_dossier, nom_sous_dossier, nom_dossier, nom_sous_dossier, nom_sous_dossier))
            print("animation_gif_faite")
        print("nouveau cycle")

    #GPIO.cleanup()
