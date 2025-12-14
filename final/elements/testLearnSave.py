# elements/testBasic.py
from Arm import Arm
import time

arm = Arm()
arm.connect()

arm.unlock()
input("Move Robot to GREEN, then hit enter")
arm.lock()

arm.printPose()
arm.learnPose("GREEN")

time.sleep(1)

arm.unlock()
input("Move Robot to RED, then hit enter")
arm.lock()

arm.printPose()
arm.learnPose("RED")

time.sleep(1)

arm.unlock()
input("Move Robot to BLUE, then hit enter")
arm.lock()

arm.printPose()
arm.learnPose("BLUE")

time.sleep(1)

arm.unlock()
input("Move Robot to 0-0, then hit enter")
arm.lock()

arm.printPose()
arm.learnPose("0-0")

time.sleep(1)

arm.unlock()
input("Move Robot to 0-1, then hit enter")
arm.lock()

arm.printPose()
arm.learnPose("0-1")

time.sleep(1)

arm.unlock()
input("Move Robot to 0-2, then hit enter")
arm.lock()

arm.printPose()
arm.learnPose("0-2")

time.sleep(1)

arm.unlock()
input("Move Robot to 1-0, then hit enter")
arm.lock()

arm.printPose()
arm.learnPose("1-0")

time.sleep(1)

arm.unlock()
input("Move Robot to 1-1, then hit enter")
arm.lock()

arm.printPose()
arm.learnPose("1-1")

time.sleep(1)

arm.unlock()
input("Move Robot to 1-2, then hit enter")
arm.lock()

arm.printPose()
arm.learnPose("1-2")

time.sleep(1)

arm.savePoses()
arm.disconnect()

