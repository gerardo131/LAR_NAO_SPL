import math
def posicion(ballinfo, robotframe):
    #print "robotframe" ,robotframe[0],robotframe[1],robotframe[2],robotframe[4]
    #print "ballinfo",ballinfo[0],ballinfo[1]
    pos=[0.0,0.0]
    cx= ballinfo[0]
    cy= ballinfo[1]
    x= robotframe[0]
    y= robotframe[1]
    z= robotframe[2]
    wy= robotframe[4]
    Theta1=0.0
    Ex1T=0.0
    Ex2T=0.0
    Ey1T=0.0
    Ey2T=0.0
    poscamerapiso= [x, y]
    poscen = [0.0,0.0]
    
    #Calculo de los valores en el eje "y" de la imagen
    Theta1= math.pi/2 - wy
    h1= z/math.cos(Theta1)
    co1=h1*math.sin(Theta1)
    poscen[0]= co1+x
    poscen[1]= y

    #extremo  del eje "y" de la parte positiva de la imagen
    Ex1T=Theta1-math.radians(23.82)
    h2 = z/math.cos(Ex1T)
    co2 = h2*math.sin(Ex1T)
    posxEx1 = x+co2

    #extremo del eje "y" de la parte negativa de la imagen
    Ex2T=Theta1+math.radians(23.82)
    h3 = z/math.cos(Ex2T)
    co3 = h3*math.sin(Ex2T)
    posxEx2 = x+co3
    
    #eleccion de espacio en imagen para obtener valores de "x" en el plano del piso en metros
    if cy < 0.0:
       d = posxEx2 - poscen[0] 
       comp1 = (-1* cy *d)/math.radians(23.82)
       pos[0] = poscen[0]+comp1
    else:
       d = poscen[0]-posxEx1
       comp1 = (cy *d)/math.radians(23.82)
       pos[0] = poscen[0]-comp1
    
    #Calculo de valores en "x" de la imagen
    Ey1T= math.radians(30.485)
    h4= h1/math.cos(Ey1T)
    co4=h4*math.sin(Ey1T)
    posy1= co4+y #extremo eje "x" parte positiva
    posy2= y-co4 #extremo eje "x" parte negativa
   
    #elecion del espacio en la imagen para obtener valores en "y" del plano del piso en metros
    if cx >= 0.0:
       dy = posy1-poscen[1]
       comp2 = (cx *dy)/math.radians(30.485)
       pos[1] = poscen[1]+comp2
    else:
       dy = poscen[1]-posy2
       comp2 = (-1*cx *dy)/math.radians(30.485)
       pos[1] = poscen[1]-comp2
    #devolicion del vector posicion  del centro de la pelota en el plano del piso en metros 
    return pos
