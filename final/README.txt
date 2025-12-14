Use scripts in order to create venv and install dependencies.

"my_robot.json" is expected by the program to be in: ~/.cache/huggingface/lerobot/calibration/robots/so101_follower/

align.py takes a picture from the known "CAMERA" position so you can align the grid with the robot (roughly 7 inches away, camera method is more precise)

testLearnSave.py will is to recalibrate the robots known cell positions and sorting buckets

testExecute.py activates the sorting program, in the order green -> red -> blue


