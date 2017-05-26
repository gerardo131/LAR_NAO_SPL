import metodos_num

ary_puntos=[  [-3.3 ,7.5] , [ -4.41 ,11.11 ] , [5.68,10.58], [5.3,7.5]  ]
	

def punto_bezier_Cua( t ) :

	p1x = ary_puntos[0][0]*(1-t)**3 
	p2x = 3*ary_puntos[1][0]*t* (1-t)**2 
	p3x = 3*ary_puntos[2][0]*(1-t)* t**2
	p4x = ary_puntos[3][0]*t**3

	p1y = ary_puntos[0][1]*(1-t)**3 
	p2y = 3*ary_puntos[1][1]*t* (1-t)**2 
	p3y = 3*ary_puntos[2][1]*(1-t)* t**2
	p4y = ary_puntos[3][1]*t**3


	return [ p1x+p2x+p3x+p4x,p1y+p2y+p3y+p4y ]

def der_punto_bezier(t):

	x=[0.0,0.0,0.0]
	y=[0.0,0.0,0.0]

	for i in [0,1,2]:
		x[i]=ary_puntos[i+1][0]-ary_puntos[i][0]
		#print "componentes x",x[i]
		y[i]=ary_puntos[i+1][1]-ary_puntos[i][1]
		#print "componentes y",y[i]

	d_x =3*( x[0] *(1-t)**2 + 2*x[1]*(1-t)*t + x[2]*t**2 )

	d_y = 3*( y[0] *(1-t)**2 + 2*y[1]*(1-t)*t + y[2]*t**2 )
	#print "derivada de la curva = ",d_x,"    " ,d_y  
	return d_y/d_x

def encontrar_t(v_dir):

	A_p=[0,0,0]
	####-------------sacar cueficientes --------###[     ]
	for i in [0,1,2] :
		A_p[i]=(ary_puntos[i+1][0]-ary_puntos[i][0])*v_dir[0] + (ary_puntos[i+1][1]-ary_puntos[i][1])*v_dir[1]
	X_2=A_p[0]-2*A_p[1]+A_p[2]
	X_1=2*(A_p[1]-A_p[0])
	X_0=A_p[0]


	####---------------Resolver--------------------

 	return metodos_num.secante (0,1,X_2,X_1,X_0)


###el punto de la derivada es pensando en que la pelota esta en en el origen 

def  punto_pelota (v_dir,radio ):

	t=encontrar_t(v_dir)
	#print "t  = " ,t 
	der_punto=der_punto_bezier(t)

	y =radio**2 /(der_punto**2+1) 
	x = radio**2-y
	y=y**.5
	x=x**.5
### se hace un camio a de las cosdenadas en 2D de la imgen a las cordenadas 3D de NAO
	return [y/100.0,x/100.0]


def punto_golpe( v_dir):

 	t=encontrar_t(v_dir)

 	####---------------Cambio de imagen de 2D a 3D
 	vX=punto_bezier_Cua(t)[1]/100.0
 	vY=punto_bezier_Cua(t)[0]/100.0


 	return [vX,vY]


	####-------------------------------------------




#print punto_bezier_Cua(  ary , 0.71)

print punto_golpe([0.62,0.79] )
print punto_pelota([0.62,0.79],2.5)

