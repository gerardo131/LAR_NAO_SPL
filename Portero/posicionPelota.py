#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

def posicion(BallInfo, RobotFrame):
    print "En módulo posicionPelota: "
    print "RobotFrame: ",RobotFrame[0], RobotFrame[1], RobotFrame[2], RobotFrame[4]
    print "BallInfo: ", BallInfo[0], BallInfo[1]
    '''
        posicion // Posición de la pelota en el plano XY
        centro_x, centro_y // Coordenadas del centro de la pelota en el plano de la imagen
        x, y, z, wy // Posisición de la cámara con respecto a ROBOT_FRAME
        Theta //
    '''

    posicion = [0.0, 0.0]
    centro_x = BallInfo[0]
    centro_y = BallInfo[1]
    x = RobotFrame[0]
    y = RobotFrame[1]
    z = RobotFrame[2]
    wy = RobotFrame[4]
    Theta = 0.0
    Ex1T = 0.0
    Ex2T = 0.0
    Ey1T = 0.0

    Ey2T = 0.0 # No se usa esta variable

    poscamarapiso = [x, y] # No se usa esta variable
    # Vector para guardar las coordenadas del centro de la pelota
    poscen = [0.0, 0.0]

    # Cálculo de los valores en el eje "y" de la imagen
    Theta = math.pi / 2 - wy
    h1 = z / math.cos(Theta)
    co1 = h1 * math.sin(Theta)
    poscen[0] = co1 + x
    poscen[1] = y

    # Extremo  del eje "y" de la parte positiva de la imagen
    Ex1T = Theta - math.radians(23.82)
    h2 = z / math.cos(Ex1T)
    co2 = h2 * math.sin(Ex1T)
    posxEx1 = x + co2

    # Extremo del eje "y" de la parte negativa de la imagen
    Ex2T = Theta + math.radians(23.82)
    h3 = z / math.cos(Ex2T)
    co3 = h3 * math.sin(Ex2T)
    posxEx2 = x + co3

    # Eleccion de espacio en imagen para obtener valores
    # de "x" en el plano del piso en metros
    if centro_y < 0.0:
        d = posxEx2 - poscen[0]
        comp1 = (-1* centro_y *d) / math.radians(23.82)
        posicion[0] = poscen[0] + comp1
    else:
        d = poscen[0] - posxEx1
        comp1 = (centro_y * d) / math.radians(23.82)
        posicion[0] = poscen[0] - comp1

        # Cálculo de valores en "x" de la imagen
        Ey1T = math.radians(30.485)
        h4 = h1/math.cos(Ey1T)
        co4 = h4 * math.sin(Ey1T)
        posy1 = co4 + y #extremo eje "x" parte positiva
        posy2 = y - co4 #extremo eje "x" parte negativa

        # Elección del espacio en la imagen para obtener valores
        # en "y" del plano del piso en metros
        if centro_x >= 0.0:
            dy = posy1 - poscen[1]
            comp2 = (centro_x * dy) / math.radians(30.485)
            posicion[1] = poscen[1] + comp2
        else:
            dy = poscen[1] - posy2
            comp2 = (-1 * centro_x * dy) / math.radians(30.485)
            posicion[1] = poscen[1] - comp2
            #devolicion del vector posicion  del centro de la pelota en el plano del piso en metros
            return posicion
