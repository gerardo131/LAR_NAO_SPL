import sys
import math
import time
from naoqi import ALProxy
import motion

def movimientoPortero( lado_protegido,IPNAO):


    if lado_protegido < 0 :
        apoyo="L"
        fuerza="R"
        fac_mul = 1
    elif lado_protegido >0 :
        apoyo="R"
        fuerza="L"
        fac_mul = -1
    try:
        motionProxy = ALProxy("ALMotion",IPNAO,9559)
    except Exception,e:
        print "No se puede crear el proxy"
        print "Error was: ",e

    ##---------------------------------
    motionProxy.setFallManagerEnabled(False)

    dx         = 0.07                    # translation axis X (meter)
    dy         = 0.09                    # translation axis Y (meter)
    dwx        = 0.00                 # rotation axis X (rad)
    dwy        = 0.15                    # rotation axis Y (rad)

    ##----------------balance de caida ----------------------------------

    ##****************separacion de pieseses**************************

    path =[0.0, 0.05*fac_mul, 0.0, 0.0,  0.0, 0.0] # movimiento a la izquierda
    timeOneMove  = .05 #seconds
    times=timeOneMove
    effector   = apoyo+"Leg"
    space      =  motion.FRAME_ROBOT
    axisMask   = 63
    isAbsolute = False
    motionProxy.positionInterpolation(effector, space, path,axisMask, times, isAbsolute)



    path =[0.0, fac_mul*dy, -0.01,  dwx,  0.0, 0.0] # movimiento a la izquierda
    timeOneMove  = .2 #seconds
    times=timeOneMove
    effector   = "Torso"
    space      =  motion.FRAME_ROBOT
    axisMask   = 63
    isAbsolute = False
    motionProxy.post.positionInterpolation(effector, space, path, axisMask, times, isAbsolute)

    ##-------------------debilitar caida con movimientos en las piernas--------------------------------------------


    ##*************************brazo de apoyo*******************

    motionProxy.post.angleInterpolation([apoyo+"ShoulderRoll", apoyo+"ShoulderPitch", apoyo+"ElbowRoll", apoyo+"ElbowYaw", apoyo+"WristYaw"],[74.1*3.1416/180*fac_mul, 0.0*3.1416/180, -26.0*3.1416/180*fac_mul, -103*3.1416/180*fac_mul, -91*3.1416/180*fac_mul],[0.2, 0.2, 0.2, 0.2, 0.2],True )    
    motionProxy.setStiffnesses(apoyo+"ElbowRoll",0.7)

    #***************pierna derecha******************************
    path =[0.0, 0.0, -0.005, 0.0,  0.0, 0.0] 
    timeOneMove  = .1
    times=timeOneMove
    effector   = fuerza+"Leg"
    space      =  motion.FRAME_ROBOT
    axisMask   = 63
    isAbsolute = False
    motionProxy.post.positionInterpolation(effector, space, path,axisMask, times, isAbsolute)

    #********************pierna Izquierda ***************************************
    path = [-0.01, 0.0, 0.08,  0.0,  0.0, 0.0] 
    timeOneMove  = .15
    times=timeOneMove
    effector   = apoyo+"Leg"
    space      =  motion.FRAME_ROBOT
    axisMask   = 63
    isAbsolute = False
    motionProxy.post.positionInterpolation(effector, space, path,axisMask, times, isAbsolute)


    ##-----------------------------------------------------------------------------------
    motionProxy.setStiffnesses("Body",0.7)
    time.sleep(.3)

    art=[apoyo+"ShoulderRoll",apoyo+"ShoulderPitch", apoyo+"ElbowRoll",apoyo+"ElbowYaw", apoyo+"WristYaw", apoyo+"HipPitch",apoyo+"KneePitch",apoyo+"AnklePitch", fuerza+"HipPitch",fuerza+"HipRoll",fuerza+"KneePitch", fuerza+"AnklePitch", fuerza+"AnkleRoll",fuerza+"ShoulderRoll",fuerza+"ShoulderPitch",fuerza+"ElbowRoll", fuerza+"ElbowYaw",fuerza+"WristYaw",fuerza+"Hand"] 

    grados = [3.9*3.1416/180*fac_mul,-74.7*3.1416/180,-28*3.1416/180*fac_mul,-95*3.1416/180*fac_mul, 17.1*3.1416/180*fac_mul ,6.0*3.1416/180, 19.0*3.1416/180,-13*3.1416/180,
    -55.0*3.1416/180,-13.0*3.1416/180*fac_mul,65.0*3.1416/180,32.2*3.1416/180, 0.0*3.1416/180*fac_mul,-0.2*3.1416/180*fac_mul,72.1*3.1416/180,62.0*3.1416/180*fac_mul,
72.7*3.1416/180*fac_mul,-96.0*3.1416/180*fac_mul,0.0 ]  

    motionProxy.post.angleInterpolation(art,grados,[0.4,0.4,0.4, 0.4,0.4,0.4, 0.4, 0.4,0.4,0.4, 0.4, 0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4],True)
    time.sleep(3.0)
 


	        
