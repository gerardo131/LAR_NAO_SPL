import punto_golpe
import Actuador_Patada
import PelotaModule
import time
import sys
import math
from naoqi import ALProxy

contador=0
Pelota = None

def pasosAjuste(metrosX,metrosY,NAO_IP):
    try:
        motionProxy = ALProxy("ALMotion",NAO_IP,9559)
    except Exception,e:
        print "No se puede crear el proxy de ALMotion"
        print "Error was: ",e

    try:
        postureProxy = ALProxy("ALRobotPosture",NAO_IP,9559)
    except Exception, e:
        print "No se puede crear el proxy de ALRobotPosture"
        print "Error was: ", e
    postureProxy.goToPosture("StandInit", 0.5)

    # Ejemplo para mostrar como avanzar de forma perzonalizada
    # Las unidades son en metros y radianes
    # Los pasos son personalizados dependiendo de la distancia a recorrer
    # Se redondean los valores solo a 3 decimales
    x = round(metrosX,3)
    y = round(metrosY,3)

    #------------- Restricciones para avances en x ----------------------
    if x >= 0.05 and x <= 0.1: #Entre 5 y 10 cm, restarle al avance 3 cm
       x  = x/2
       S_X = ["MaxStepX",0.025] #Pasos max de 2.5 cm
    else:
       if x > 0.1: #Valores mayores a 10 cm
          x= x/2
          S_X = ["MaxStepX",0.04] #Pasos de 4 cm
       else: #Valores menores a 5 cm
          if x < 0.005 and x >= 0.0: #Es menor 1/2 cm
             x = 0.0
             S_X = ["MaxStepX",0.002] #Pasos de 0.3 cm
          else:
             if x < 0.0: #Retroceder la distancia solicitada
                x = x-0.005
                S_X = ["MaxStepX",0.02] #Pasos de 2 cm
             else: # x es mayor a 1/2 cm, avanzar solo la mitad de lo que se solicita
                x = x/2
                S_X = ["MaxStepX",0.02] #Pasos de 1 cm

    #---------------- Restricciones para avanes en y --------------------
    # Lo maximo de separacion un pie del otro son 12 cm,
    # si hay 10 cm de separacion entre pies en standInit a lo mas se podra separa 2 cm por pasos en Y
    S_Y = ["MaxStepY",0.12] #Pasos max de 2cm
    y = y / 2
    if y > -0.05 and y < 0.05: # distancias entre -5 y 5 cm
       if y >= -0.01 and y<= 0.01: #distancias ente -1 y 1 cm
          S_Y = ["MaxStepY",0.105] #Pasos max de 0.5 cm
       else:
          S_Y = ["MaxStepY",0.11] #Pasos max de 1cm
    else:
       if y < -0.20 or y >0.20: # distancias menores de -20 cm o mayores a 20 cm
          S_Y = ["MaxStepY",0.140] #Pasos max de 4cm

    print "Valor de x : ",x, "Valor de y: ", y

    #-------------------Movimientos-------------------------------------

    #Movimiento en x
    motionProxy.moveTo(x, 0.0, 0.0,[S_X])

    #Movimiento en y
    motionProxy.moveTo(0.0, y, 0.0,[S_Y])

##-----------------------------------------------------------------------------------------------------------------


def ajusteZ(Rot_Z,NAO_IP):

    try:
        motionProxy = ALProxy("ALMotion",NAO_IP,9559)
    except Exception,e:
        print "No se puede crear el proxy de ALMotion"
        print "Error was: ",e

    try:
        postureProxy = ALProxy("ALRobotPosture",NAO_IP,9559)
    except Exception, e:
        print "No se puede crear el proxy de ALRobotPosture"
        print "Error was: ", e

    postureProxy.goToPosture("StandInit", 0.5)

    #Correccion en Z
    theta=round(Rot_Z,5)
    theta = theta*(-1)
    S_T = ["MaxStepTheta",0.2618] #Maximo de rotacion en el pie de 15 grados
    #Movimiento en y
    motionProxy.moveTo(0.0,0.0,theta,[S_T])


##---------------------------------------------------------------------------------------------------------------

def consultaDesviacion(NAO_IP):
  try:
    brujula = ALProxy("VisualCompass",NAO_IP, 9559)
    desviacion = brujula.getDesviacionZ()
  except Exception,e:
    print "No se puede crear el proxy de ALVisualCompass"
    print "Error was: ",e
    desviacion = 0.0
  print "--------------------------------"
  print "desviacion Z", desviacion
  print "---------------------------------"

  # desviacion = 0.0
  if desviacion < -2.999*math.pi/180  or desviacion > 2.999*math.pi/180:
    ajusteZ(desviacion,NAO_IP)
    return False
  else:
    print "La desviación en Z no es considerable: ", (desviacion*180)/math.pi, "\n"
    return True

##----------------------------------------------------------------------------------------------------------------

def DistanciaPtoPatada(posPel, posContacto,NAO_IP):
  #Obtener las distancias para ajustarse
  global contador
  contador+=1

  dx = round(posPel[0]-posContacto[0],4)
  dy = round(posPel[1]-posContacto[1],4)
  print "dx : ", dx,"\ndy: ", dy
  realizar_patada=False
  ##--------------Condiciones X--------------------
  if dx <= 0.02 and dx >= 0.015 :
    print "en x es adecuado" , dx
    dx=0.0
  else :
    dx = dx-.015
    if abs (dx) <= 0.003:
      dx=0.0
    print "en x no es adecuado", dx
  ##---------------condiciones Y--------------------
  if dy >-0.02 and dy<0.00:
    print "en y es adecuado ", dy
    dy = 0.0
  else:
    print "en y no es adecuado", dy
  ##----------------------------------------------

  if dx<=0.0 and dy==0.0 and  dx>=-0.015:
    realizar_patada=True
  else:
    pasosAjuste(dx,dy,NAO_IP)
    realizar_patada=False
  ##--------------Condiciones Z-----------------------
  '''if not consultaDesviacion(NAO_IP):
    print "La desviacion en Z es considerable. Se realizo una rotacion \n"
    realizar_patada=False
  '''
  ##--------------------------------------------------
  if contador >= 2 :
    return True
  else :
    return realizar_patada
    ##-------------------------------------------------------------------------------------------------------------------


def PreparaPatada(pos,V_dirC,V_dir,NAO_IP):

    # Posicion de golpe fija en el centro de pie
    posCentroPie = [0.12,0.05]#si es para la otra pierna aqui va [0.12,-0.05]

    #Calculo de posicion en el pie del punto de contacto dependiendo de la direccion de la patada
    PC=punto_golpe.punto_golpe(V_dir)

    #Calculo correcto del punto de contacto con la pelota
    PtoContPel = punto_golpe.punto_pelota(V_dir,3.5)
    posPelota = [0.0,0.0]
    # Le quitamos el radio de la pelota para considerar al punto como la parte extrema de la pelota en X
    posPelota[0]= pos[0]-0.05
    posPelota[1]= pos[1] #+PtoContPel[1]

    #transformacion de sistema de patada a sistema de Robot
    punto_contacto_y=PC[1]+.053 #Aqui va -0.053
    punto_contacto_x = PC[0]+0.02

    #La distancia en X se considera como tope el centro golpe en el pie y la pos de la pelota en x ya transformada
    disX = posPelota[0] - posCentroPie[0]
    dcY = posPelota[1]-punto_contacto_y # Distancia para mover el pie al momento de patear

    if V_dir[0] < 0:
    	dcY += PtoContPel[1]+0.005
    elif V_dir[0]> 0:
    	dcY -= PtoContPel[1]


    print "Distancias antes de entrar a ajuste en X ", disX

    ##-----------------------------decision de mover pie-------------------
    ## !!!!Cuidaddo V_dir [0] es (x) en el sistema 2D pero (y) en sistema 3D_NAO
    ## la distacia en el eje x deceada entre el punto de contacto la pelota sera de 3cm

    if V_dir[0] < 0: #La parte de adentro del pie #para el otro pie es para la parte de afuera
        posContacto = [posCentroPie[0],punto_contacto_y]

    elif V_dir[0]>= 0: #La parte de afuera debe ser un caso especial para cuidar el choque entre piernas #es adentro cuidar choque de pies
        posContacto = [posCentroPie[0],punto_contacto_y+0.01]

    #----------------------Ajustes necesarios----------------------------
    #Calculando las distancias y haciendo ajustes necesarios
    print "Pocision de la pelota: ", posPelota, "\nPosicion del contacto Pie: ",  posContacto, "\n"

    try:
       cabeza = ALProxy("ALMotion", NAO_IP, 9559)
    except Exception, e:
       print str(e)

    global Pelota
    Pelota = PelotaModule.PelotaModule("Pelota")

    if DistanciaPtoPatada(posPelota, posContacto,NAO_IP): ## parametros de decision
           print "la distacia  es la adecuada. \nDistancia de contacto en Y",dcY
           #Mover cabeza para ver puntos alrededor del pie
           cabeza.angleInterpolation("HeadPitch",20*math.pi/180,1.0,True)
           time.sleep(0.7)
           dcY = Pelota.Pos_pelota[1]
           Actuador_Patada.patada_gol(NAO_IP,9559,dcY)
           return 1
    else :
           print "la distacia no es la adecuada\n"
           return 0
##-----------------------------------------------------------------------------------------------------------------------
