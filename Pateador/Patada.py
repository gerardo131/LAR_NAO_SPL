# -*- encoding: UTF-8 -*-

import sys
import time
import math
import punto_golpe
import PelotaModule
import Prepara_Patada
import caminata

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser


# Global variable to store the Pelota module instance
Pelota = None


def Patada(v_direccionC,v_direccion,NAO_IP,PORT):
    pip=NAO_IP,
    pport=PORT

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       NAO_IP,         # parent broker IP
       9559)       # parent broker port

    #Create a proxy to ALVideoDevice

    try:
        mover = ALProxy("ALMotion",NAO_IP,9559)
        postura = ALProxy("ALRobotPosture",NAO_IP,9559)
        cameraModule = ALProxy( "ALVideoDevice", NAO_IP, 9559)

    except Exception, e:
      print "Error when creating camera module proxy:"
      print str(e)
      exit(1)

    postura.goToPosture("StandInit",1.0)
    #caminata.caminata(NAO_IP) 
    mover.moveTo(0.45,0.0,0.0,[["MaxStepX",0.06]])
    if Prepara_Patada.consultaDesviacion(NAO_IP) == False :
        print "Se realiza desviacion"
    mover.moveTo(0.4,0.0,0.0,[["MaxStepX",0.06]])
    if Prepara_Patada.consultaDesviacion(NAO_IP) == False :
        print "Se realiza desviacion"
    #------------------------------------------
    
    #Mover cabeza para ver puntos alrededor del pie
    mover.angleInterpolation("HeadPitch",20*math.pi/180,1.0,True)

    #Cambio de camara
    cameraModule.setParam(18, 1)
    
    #time.sleep(0.5)
    # ----------------- Inicio de la deteccion de la pelota-------------------------
    global Pelota
    Pelota = PelotaModule.PelotaModule("Pelota")

    try:
        #Verificando que realmente vea una pelota
        while Pelota.Pos_pelota[0] == 0.0 :
            time.sleep(0.5)
        print "pocision pelota antes de patada:", Pelota.Pos_pelota
        
        while   Prepara_Patada.PreparaPatada(Pelota.Pos_pelota,v_direccionC, v_direccion,NAO_IP) == 0 :
			#Entra aqui cuando no se ha podido realizar la patada
            postura.goToPosture("StandInit",1.0) 
            mover.angleInterpolation("HeadPitch",20*math.pi/180,1.0,True)
            time.sleep(1.3) #Tiempo de espera para volver a leer una posicion
            print "pocision pelota antes de patada:", Pelota.Pos_pelota
            
    except KeyboardInterrupt:
        #print
        #print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)
    postura.goToPosture("Crouch",0.4)
    mover.setStiffnesses("Body",0.0)



if __name__ == "__main__":
	NAO_IP ="127.0.0.1"
	#Patada([0.0,0.1],[-0.42,0.91],NAO_IP,9559)
	Patada([0.0,0.1],[-0.42,0.91],NAO_IP,9559)


