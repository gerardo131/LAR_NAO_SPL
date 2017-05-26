# -*- encoding: UTF-8 -*-

import sys
import math
import time
from naoqi import ALProxy


def caminata(robotIP):
    PORT = 9559

    try:
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ",e
        sys.exit(1)

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
        redBallTracker = ALProxy("ALRedBallTracker", robotIP, PORT)
        brujula = ALProxy("VisualCompass",robotIP, 9559)
        camara= ALProxy("ALVideoDevice",robotIP,9559)
        camara.setParam(18,0)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    try:

        if redBallTracker.isActive():
            redBallTracker.stopTracker()

        motionProxy.setStiffnesses("Body", 1.0)
        postureProxy.goToPosture("StandInit",0.4)
        motionProxy.angleInterpolation("HeadPitch",20*3.14/180,1.0,True )

        # Then, start tracker.
        redBallTracker.startTracker()

        acomulador = 1.0

        tiempo_espera=1.0
        tiempo=tiempo_espera


        while tiempo > 0.0:
            acomulador = 0
            posicion_pelota=[0,0,0]

            if redBallTracker.isNewData():
                posicion_pelota = redBallTracker.getPosition()

                print posicion_pelota
                for i in posicion_pelota :
                    print i
                    acomulador+=i
            if(acomulador == 0.0):
                tiempo -=0.01
                time.sleep(0.01)
            else :
                print "me movi"
                paso=0.06
                S_X = ["MaxStepX",paso]
                frecuencia= ["MaxStepFrequency",0.5]
                altura = ["StepHeight",0.04]

                pos_norma_pelota=1/(posicion_pelota[0]**2+posicion_pelota[1]**2)**.5
                vec_pelota_norma=[posicion_pelota[0]*pos_norma_pelota,posicion_pelota[1]*pos_norma_pelota]

                redBallTracker.stopTracker()
                
                posicionJoin=motionProxy.getAngles("Head",True)
                motionProxy.angleInterpolation(["HeadYaw","HeadPitch"],[0,0],[.2,.2],True)
                desvicion=0.0#-1*brujula.getDesviacionZ()
                motionProxy.angleInterpolation(["HeadYaw","HeadPitch"],posicionJoin,[.3,.3],True)
                motionProxy.moveTo(vec_pelota_norma[0]*paso*3,vec_pelota_norma[1]*paso*3,desvicion,[S_X,frecuencia])

                redBallTracker.startTracker()
                tiempo=tiempo_espera

    except KeyboardInterrupt:
        redBallTracker.stopTracker()
        postureProxy.goToPosture("Crouch",0.4)
        motionProxy.setStiffnesses("Body", 0.0)
   # motionProxy.angleInterpolation(["HeadYaw","HeadPitch"],posicionJoin,[.2,.2],True)
    desvicion=0.0#-1*brujula.getDesviacionZ()
    motionProxy.moveTo(0.0,0.0,desvicion)

    redBallTracker.stopTracker()    
    # Will block until move Task is finished

    ########
    # NOTE #
    ########
    # If moveTo() method does nothing on the robot,
    # read the section about walk protection in the
    # Locomotion control overview page.

