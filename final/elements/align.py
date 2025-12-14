from Camera import Camera
from Arm import Arm
import time

cam = Camera(index=0)
cam.connect()

arm = Arm()
arm.connect()
arm.loadPoses()

arm.executePose("CAMERA")

time.sleep(3)

cam.snapshot("alignment.png")

print("Image Saved!")

cam.disconnect()
arm.disconnect()
