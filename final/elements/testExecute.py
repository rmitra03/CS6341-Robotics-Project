import time
from Camera import Camera
from Arm import Arm

cam = Camera(index=0)
cam.connect()

arm = Arm()
arm.connect()
arm.loadPoses()

#Picture
arm.executePose("CAMERA")
time.sleep(1.5)

x, y = cam.getColorCell("green", "currImage.png")

command = str(x) + "-" + str(y)

arm.Grip(20)

time.sleep(1)

arm.executePose(command)
time.sleep(1.5)
arm.Grip(7.5)
time.sleep(1)
arm.executePose("CAMERA")
time.sleep(1.5)
arm.executePose("GREEN")
time.sleep(1.5)
arm.Grip(20)
time.sleep(1)
arm.executePose("CAMERA")
time.sleep(1.5)

arm.executePose("CAMERA")
time.sleep(1.5)

x, y = cam.getColorCell("red", "currImage.png")

command = str(x) + "-" + str(y)

arm.Grip(20)

time.sleep(1)

arm.executePose(command)
time.sleep(1.5)
arm.Grip(7.5)
time.sleep(1)
arm.executePose("CAMERA")
time.sleep(1.5)
arm.executePose("RED")
time.sleep(1.5)
arm.Grip(20)
time.sleep(1)
arm.executePose("CAMERA")
time.sleep(1.5)

arm.executePose("CAMERA")
time.sleep(1.5)

x, y = cam.getColorCell("blue", "currImage.png")

command = str(x) + "-" + str(y)

arm.Grip(20)

time.sleep(1)

arm.executePose(command)
time.sleep(1.5)
arm.Grip(7.5)
time.sleep(1)
arm.executePose("CAMERA")
time.sleep(1.5)
arm.executePose("BLUE")
time.sleep(1.5)
arm.Grip(20)
time.sleep(1)
arm.executePose("CAMERA")
time.sleep(1.5)


'''
arm.executePose("GREEN")
time.sleep(3)
arm.executePose("CAMERA")
time.sleep(3)

arm.executePose("RED")
time.sleep(3)
arm.executePose("CAMERA")
time.sleep(3)

arm.executePose("BLUE")
time.sleep(3)
arm.executePose("CAMERA")
time.sleep(3)
'''

input("Press Enter to Exit")
      
arm.disconnect()
cam.disconnect()

