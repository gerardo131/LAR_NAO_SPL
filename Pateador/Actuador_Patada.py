import sys
import time
from naoqi import ALProxy

def patada_gol(IpNao,port, py ): 



	try:

	    mover = ALProxy("ALMotion",IpNao,port)
	    postura = ALProxy("ALRobotPosture",IpNao,port)
	    tts=ALProxy("ALTextToSpeech",IpNao,port)

	except Exception,e:
	    print"ERROR :",e
	    sys.exit(1)

	mover.setStiffnesses("Body",1.0)
	postura.goToPosture("StandInit",1.0)

	##------------

	    
	mover.wbEnable(True)
	######-------------------balance-------------
	mover.wbFootState("Fixed","Legs")

	mover.wbEnableBalanceConstraint(True,"RLeg")

	mover.wbEnableEffectorOptimization("LLeg",True)
	####-----------------------------------------
	

	####------------Postura de goleador-----------
	mover.wbGoToBalance("RLeg",2.0)
	mover.wbFootState("Free","LLeg")
	RJoinNames=[
	            
	            "RHipYawPitch",
	            "RHipRoll",
	            "RHipPitch",
	            "RKneePitch",
	            "RAnklePitch",
	            "RAnkleRoll"
	            ]
	LJoinNames=[
	            
	            "LHipYawPitch",
	            "LHipRoll",
	            "LHipPitch",
	            "LKneePitch",
	            "LAnklePitch",
	            "LAnkleRoll"
	            ]  
	RJoinNames_Arm =[
						"RShoulderPitch",
						"RShoulderRoll",
						"RElbowYaw",
						"RElbowRoll"
					] 
	RJoinNames_Arm =[
						"RShoulderPitch",
						"RShoulderRoll",
						"RElbowYaw",
						"RElbowRoll"
					]        
	Roriginal_angles_Arm=mover.getAngles(RJoinNames_Arm,False)					
	Roriginal_angles = mover.getAngles(RJoinNames,False)
	Loriginal_angles = mover.getAngles(LJoinNames,False)
	Roriginal_angles_Arm=mover.getAngles(RJoinNames_Arm,False)


	## mover brazo para balance ----------------------------

   	anglelista=[0.0 ,-70.0 *3.14/180,Roriginal_angles_Arm[2],5.0*3.14/180]
   	time=[1.0,1.0,1.0,1.0]
   	#mover.angleInterpolation(RJoinNames_Arm,anglelista,time,True)

   	###--------------------------------

	print "rodilla",Loriginal_angles[3] ,"tobillo",Loriginal_angles[4]
	joints = ["RShoulderPitch","RShoulderRoll","RElbowYaw","RElbowRoll","LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll"]
	angulos = [73.4*3.14/180 ,-71 *3.14/180,83.1*3.14/180 ,20.6*3.14/180,25.5*3.14/180 ,-18*3.14/180,-12.9*3.14/180 ,-57*3.14/180]
	times = [1.0, 1.0, 1.0, 1.0,1.0, 1.0, 1.0, 1.0]
	#mover.angleInterpolation(joints,angulos,times,True)

	effectorName = "LLeg"
	axisMask     = 63
	space        = 2            
	times =[1.0,3.0,5.0]

	
	targetList = [ [0.0, 0.0, 0.05, 0.0, 0.0, 0.0],
					[0.0, py, 0.05, 0.0, 0.0, 0.0],
					[-0.05, py , 0.05, 0.0 , 0.0 , 0.0]
	             ]
	efector = "RShoulderRoll"
	mover.positionInterpolation(effectorName, space, targetList,axisMask, times, False)

	######-----------------------------------------------------------------


	######-------------------tiro a gol-----------------------
	Joins=["LHipPitch","LAnklePitch","LKneePitch"]
	angles=[-60.0*3.14/180, 25.0*3.14/180,10.0*3.14/180] #Loriginal_angles[4]]
	mover.angleInterpolationWithSpeed(Joins,angles,1.0)

	######-----------------------------------------------------------        


	###-------Posicion Original-----------


	times=[1.5,1.5,1.5,1.5,1.5,1.5]        

	mover.angleInterpolationWithSpeed("LAnklePitch",Loriginal_angles[4],0.3)
	mover.angleInterpolation(LJoinNames,Loriginal_angles,times,True)
	mover.angleInterpolation(RJoinNames,Roriginal_angles,times,True)

	###-----------------------------------------------------------


	#tts.say("me caigo")
	mover.wbEnable(False)
	#postura.goToPosture("Stand",0.4)
	postura.goToPosture("StandInit",0.4)	
	postura.goToPosture("Crouch",0.8)
	mover.setStiffnesses("Body",0.0)


#patada_gol("127.0.0.1",9559,0.017)	            
