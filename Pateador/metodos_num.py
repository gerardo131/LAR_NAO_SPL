
def evaluacion(x_2 ,  x_1, x_0,  x) :

		return x_2*x*x +  x_1*x + x_0 



def  abso(p):

	if p<0 :
		return -1*p
	else :
		return p


def secante ( haig, law , x_2, x_1, x_0) : 

	error=0.00000001

 	nueva = haig-( (haig-law)/ (evaluacion(x_2,x_1,x_0,haig ) - evaluacion(x_2,x_1,x_0,law ) ) )*evaluacion(x_2,x_1,x_0,haig )
	vieja = haig

	#print "ffff", abso ((nueva- vieja)*100.0/nueva)

	while  error < abso( (nueva- vieja)*100.0/nueva  ) :
	

		if  evaluacion(x_2,x_1,x_0,nueva ) > 0 :
			haig=nueva
		else: 
			law=nueva
		vieja=nueva
		nueva = haig-( (haig-law)/ (evaluacion(x_2,x_1,x_0,haig ) - evaluacion(x_2,x_1,x_0,law ) ) )*evaluacion(x_2,x_1,x_0,haig )	
	
	return nueva





