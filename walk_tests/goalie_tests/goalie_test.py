# -*- encoding: UTF-8 -*-
import time
import math

from naoqi import ALProxy

# Regresa la dirección de la pelota
def direction(NAOIP, NAOPORT):
    #----Funcion deteccion de movimiento de pelota -------
    try:
        redBallProxy = ALProxy("ALRedBallDetection",NAOIP,NAOPORT)
        memProxy = ALProxy("ALMemory", NAOIP, NAOPORT)
    except Exception, e:
        print 'No se pudo crear proxy', e

    period = 1
    precision = 0.0
    redBallProxy.subscribe("redBallDetected", period, precision)
    time.sleep(1.0)
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
    print "Iniciando detección"
    # Del centro de la imagen a la izquierda son grados negativos
    while True:
        #time.sleep(0.1)
        info_pelota = memProxy.getData("redBallDetected")
        angulo_x = info_pelota[1][0]
        angulo_y = info_pelota[1][1]
        desplazamiento = angulo_y_inicial - angulo_y
        contador += 1
        # print contador
        # print "desplazamiento",desplazamiento, "angulo_y", angulo_y
        # Cuando se obtiene un dezplazamiento positivo indica
        # que la pelota se esta moviendo hacia atras
        # por lo que indica que no tenia un valor correcto en su primer
        # deteccion entonces se debe actualizar en las variables iniciales
        if desplazamiento > 0.0:
            angulo_y_inicial = angulo_y
            angulo_x_inicial = angulo_x
            desplazamiento = angulo_y_inicial - angulo_y

        if math.fabs(desplazamiento)<0.052 :
            #no hacer nada
            contador = contador

        else:
            if angulo_x_inicial < angulo_x:
                direccion = "izquierda"
                print "Izquierda ", angulo_x
            else:
                direccion = "derecha"
                print "Derecha ", angulo_x
            break

    redBallProxy.unsubscribe("redBallDetected")
    print "Termina detección, con ", contador, " detecciones"

    return direccion
    #------Termina deteccion de movimiento de pelota--------

def main():
    #--------------Funcion main-----------------------------
    NAOIP = '127.0.0.1'
    NAOPORT = 9559
    try:
        motion = ALProxy('ALMotion', NAOIP, NAOPORT)
        posture = ALProxy('ALRobotPosture', NAOIP, NAOPORT)
        cam = ALProxy("ALVideoDevice", NAOIP,NAOPORT)
    except Exception, e:
        print 'No se pudo crear el proxy', e

    #Se hace el cambio a la camara de abajo
    cam.setParam(18,0)
    motion.setStiffnesses("Body",1.0)
    posture.goToPosture("StandInit", 1.0)
    #Inclina un poco la cabeza para enfocar solo la pelota
    motion.angleInterpolation("HeadPitch", 5 * 3.14 / 180, 1.0, True)
    time.sleep(1.0)

    #Funcion para obtener la dirección cuando la pelota se mueva
    direccion = direction(NAOIP, NAOPORT)
    print direccion

    # Guardamos los valores en un archivo separado por comas
    file_csv = open('output_portero.csv', 'a')
    file_csv.write(direccion + '\n')
    file_csv.close()

    time.sleep(1.0)
    posture.goToPosture("StandInit", 1.0)
    posture.goToPosture("Crouch",0.4)
    motion.setStiffnesses("Body",0.0)

    #------------------Termina función main--------------------------------

if __name__ == '__main__':
    main()
