#!/bin/bash
set -e

echo TEST ROBOT
source .venv/bin/activate

python3 - << 'EOF'
from lerobot.robots.so101_follower import SO101Follower, SO101FollowerConfig

cfg = SO101FollowerConfig(port="/dev/ttyACM0")
robot = SO101Follower(cfg)

robot.connect()
print("CONNECTED")

robot.disconnect()
print("DISCONNECTED")
EOF

echo DONE
