import sys
import time
import math

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import Calculo_Pos_Pelota


class PelotaModule(ALModule):
    """ A simple module able to react
    to facedetection events
    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        self.tts = ALProxy("ALTextToSpeech")
        self.Pos_pelota=[0.0,0.0]
        # Subscribe to the redBallDetected event:
        self.memory = ALProxy("ALMemory")
        time.sleep(0.5)
        self.memory.subscribeToEvent("redBallDetected","Pelota","onBallDetected")


    def onBallDetected(self, *_args):
        self.memory.unsubscribeToEvent("redBallDetected",
            "Pelota")
        self.tts.say("bib ")
        val = self.memory.getData("redBallDetected")
        ballinfo= val[1]
        time.sleep(0.5)
        robotframe=val[3]
        self.Pos_pelota = Calculo_Pos_Pelota.posicion(ballinfo, robotframe)
        self.memory.subscribeToEvent("redBallDetected", "Pelota","onBallDetected")
