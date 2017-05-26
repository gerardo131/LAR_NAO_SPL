# -*- encoding: UTF-8 -*-
from naoqi import ALProxy

NAOIP = "127.0.0.1" # set your Ip address here
NAOPORT = 9559

NAOIP = "192.168.2.4"

# ====================
# Create proxy to ALMemory
memoryProxy = ALProxy("ALMemory", NAOIP, NAOPORT)

# Get The Left Foot Force Sensor Values
LFsrFL = memoryProxy.getData("Device/SubDeviceList/LFoot/FSR/FrontLeft/Sensor/Value")
LFsrFR = memoryProxy.getData("Device/SubDeviceList/LFoot/FSR/FrontRight/Sensor/Value")
LFsrBL = memoryProxy.getData("Device/SubDeviceList/LFoot/FSR/RearLeft/Sensor/Value")
LFsrBR = memoryProxy.getData("Device/SubDeviceList/LFoot/FSR/RearRight/Sensor/Value")

print( "Left FSR [Kg] : %.2f %.2f %.2f %.2f" %  (LFsrFL, LFsrFR, LFsrBL, LFsrBR) )

# Get The Right Foot Force Sensor Values
RFsrFL = memoryProxy.getData("Device/SubDeviceList/RFoot/FSR/FrontLeft/Sensor/Value")
RFsrFR = memoryProxy.getData("Device/SubDeviceList/RFoot/FSR/FrontRight/Sensor/Value")
RFsrBL = memoryProxy.getData("Device/SubDeviceList/RFoot/FSR/RearLeft/Sensor/Value")
RFsrBR = memoryProxy.getData("Device/SubDeviceList/RFoot/FSR/RearRight/Sensor/Value")

print( "Right FSR [Kg] : %.2f %.2f %.2f %.2f" %  (RFsrFL, RFsrFR, RFsrBL, RFsrBR) )


# try:
#     sensores = ALProxy("ALMemory", NAOIP, NAOPORT)
# except Exception, e;
#
# def pateadorFrente()
#     print
#
# def porteroTrasero()
#
# def incio()
