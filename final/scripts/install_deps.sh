#!/bin/bash
set -e

echo INSTALL SYSTEM DEPS
sudo apt update
sudo apt install -y \
    python3-dev python3-venv \
    build-essential \
    libusb-1.0-0-dev libudev-dev \
    ffmpeg v4l-utils \
    python3-opencv

echo ACTIVATE ENV
source .venv/bin/activate

pip install --upgrade pip

echo INSTALL PYTHON DEPS
pip install "lerobot[so101]" "lerobot[vision]"
pip install feetech-servo-sdk

echo DONE
