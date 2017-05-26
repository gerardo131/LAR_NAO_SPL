from naoqi import ALProxy

NAOIP = "192.168.2.9"
NAOPORT = 9559

try:
    brujula = ALProxy("VisualCompass", NAOIP, NAOPORT)
except Exception, e:
    print e

brujula.visualDebug()
