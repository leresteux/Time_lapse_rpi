from picamera import PiCamera
from time import sleep
from time import time 
from os import system
import RPi.GPIO as GPIO
import os
from PIL import Image # pour visioner
import subprocess # pour permettre de cloturer le viewer

camera = PiCamera()
camera.resolution = (720,640)

#variables
temps_entre_photo_voulu = 3 # > 2sec (contraint de 'temps_relais') 
photos_par_dossier = 10 # >100 si creation de gif sinon ca rame et encore faut teser
creation_gif = False 

#constante
temps_avant_lancement=3# laisser le temps de monter le MEDIA
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
print("Lancement dans",temps_avant_lancement, "secondes")

sleep (temps_avant_lancement)#le temps de le MEDIA soit monté si programme au démarrage

os.makedirs('/media/julien/USBKEY/capture_%s' % nom_dossier)

print("La boucle demarre")

while 1:
    # si pas de photo prise (== nouveau cycle) alors création d'un dossier pour ce nouveau cycle
    if photos_prises == 0 :
        nom_sous_dossier += 1
        os.makedirs('/media/julien/USBKEY/capture_%s/%d' %(nom_dossier, nom_sous_dossier))
        print("creation d'un sous_dossier n°", nom_sous_dossier)
        sleep(1)
    # si nbre prises < nbre photos par dossier alors prise d'une photo
    if photos_prises < photos_par_dossier :
        GPIO.output(relay, GPIO.LOW)
        sleep(temps_relais)
        var_temps=int(time())
        camera.capture('/media/julien/USBKEY/capture_%s/%d/image%s.jpg' %(nom_dossier, nom_sous_dossier,var_temps))# indiquer image+date
        #lance un viewer avec la photo prise
        p = subprocess.Popen(['display', '/media/julien/USBKEY/capture_%s/%d/image%s.jpg' %(nom_dossier, nom_sous_dossier,var_temps)])
        sleep(temps_relais)
        
        #si temps entre photo <= 4 sec alors reste allumé
        if temps_entre_photo_voulu > 4 :
            GPIO.output(relay, GPIO.HIGH)
        
        photos_prises += 1

        print("photo prise n°", photos_prises,"/", photos_par_dossier," avant nouveau cycle (+ crea GIF si actionné)")
        sleep(temps_entre_photo_voulu)
        
        #ferme le viewer
        p.kill()

    else:
        photos_prises=0
        if creation_gif :
            var_temps=int(time())
            print("Creation du GIF n°", nom_sous_dossier)
            system('convert -delay 0.3 -loop 0 /media/julien/USBKEY/capture_%s/%d/image*.jpg /media/julien/USBKEY/capture_%s/%d/animation%d.gif' %(nom_dossier, nom_sous_dossier, nom_dossier, nom_sous_dossier, nom_sous_dossier))
            var_temps=int(time())-var_temps
            print("animation_gif_faite en ",var_temps,"sec")
        print("Dossier terminé")

    #GPIO.cleanup()
