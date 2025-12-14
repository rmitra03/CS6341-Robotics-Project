#!/bin/bash
set -e

echo RESET ENV

rm -rf .venv

sudo apt update
sudo apt install -y python3-venv build-essential python3-dev

python3 -m venv .venv

echo DONE
