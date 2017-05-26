# -*- encoding: UTF-8 -*-

import sys
import time
import math
import posicionPelota
import portero_prueba

from naoqi import ALProxy

def move(move_direction):
    try:
        move = ALProxy("ALMotion", NAOIP, NAOPORT)
    except e:
        print 'No se pudo crear proxy: ', e

    if move_direction == 'left':
       portero_prueba.movimientoPortero(-1,NAOIP)
    elif move_direction == 'right':
       portero_prueba.movimientoPortero(1,NAOIP)

# Regresa la dirección
def direction(NAOIP, NAOPORT):
    try:
        redBallProxy = ALProxy("ALRedBallDetection",NAOIP,NAOPORT)
        memProxy = ALProxy("ALMemory", NAOIP, NAOPORT)
    except Exception, e:
        print 'No se pudo crear proxy', e

    period = 1
    precision = 0.0
    redBallProxy.subscribe("redBallDetected", period, precision)
    info_pelota = memProxy.getData("redBallDetected")

    #print posicionPelota.posicion(NAOIP, NAOPORT)
    print 'En función direction:'

    # BallInfo [centerX, centerY, sizeX, sizeY]
    # centerX y centerY son las coordenadas angulares del centro de la pelota en radians
    # sizeX y sizeY son los radios, horizontal y vertical de la pelota en radianes 
    BallInfo = info_pelota[1]
    print "BallInfo: ", BallInfo

    # CameraPose_InRobotFrame
    # describe la Position6D de la cámara en el momento en que la imagen
    # fue tomada, en FRAME_ROBOT.
    #RobotFrame = info_pelota[3]

    # Desplazamiento sobre el ángulo Y, indicando que se acerca la pelota
    angulo_y_inicial = BallInfo[1]
    angulo_x_inicial = BallInfo[0]

    print "angulo_x_inicial, angulo_y_inicial", angulo_x_inicial, angulo_y_inicial
    contador = 0
    # Del centro de la imagen a la izquierda son grados negativos
    while True:
        #time.sleep(0.1)
        
        info_pelota = memProxy.getData("redBallDetected")
        angulo_x = info_pelota[1][0]
        angulo_y = info_pelota[1][1]
        desplazamiento = angulo_y_inicial - angulo_y
        contador += 1
        print contador
        print "desplazamiento",desplazamiento, "angulo_y", angulo_y
        #Cuando se obtiene un dezplazamiento positivo indica que la pelota se esta moviendo hacia atras 
        #por lo que indica que no tenia un valor correcto en su primer deteccion entonces se debe actualizar en las variables iniciales
        if desplazamiento > 0.0:
        	angulo_y_inicial = angulo_y
        	angulo_x_inicial = angulo_x
        	desplazamiento = angulo_y_inicial - angulo_y

        if math.fabs(desplazamiento)<0.052 :
            print contador
            
        else:
            if angulo_x_inicial < angulo_x:
                direccion = "left"
                print "Izquierda ", angulo_x
            else:
                direccion = "right"
                print "Derecha ", angulo_x
            break
       


        """desplazamiento = angulo_y_inicial - info_pelota[1][1]
        contador += 1
        if -0.01 < desplazamiento < 0.01:
            print contador
        elif math.fabs(desplazamiento)>0.105:
            print "Hay desplazamiento:", desplazamiento, "contador: ", contador

            if angulo_x_inicial < info_pelota[1][0]:
                direction = "left"
                print "left", info_pelota[1][0]
            elif angulo_x_inicial > info_pelota[1][0]:
                direction = "right"
                print "right", info_pelota[1][0]"""
            #break

    redBallProxy.unsubscribe("redBallDetected")

    return direccion

if __name__ == '__main__':
    NAOIP = '127.0.0.1'
    NAOPORT = 9559

    try:
        motion = ALProxy('ALMotion', NAOIP, NAOPORT)
        posture = ALProxy('ALRobotPosture', NAOIP, NAOPORT)
        cam = ALProxy("ALVideoDevice", NAOIP,NAOPORT)
    except Exception, e:
        print 'No se pudo crear el proxy', e

    cam.setParam(18,0)
    posture.goToPosture("StandInit", 1.0)
    motion.angleInterpolation("HeadPitch", 5 * 3.14 / 180, 1.0, True)
    time.sleep(1.0)
    #motion.setFallManagerEnabled(False)
    direccion = direction(NAOIP, NAOPORT)
    print direccion
    move(direccion)
    #print 'Posición hacia donde se va a mover', target[0], target[1]
    #motion.moveTo(target[0], target[1], 0.0)
