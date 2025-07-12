#!/bin/bash
echo "Starting installation script..."
cd /home/ubuntu/prodapp || exit 1

echo "Installing dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv

python3 -m venv venv
source venv/bin/activate

echo "Installing Python packages..."
pip install -r requirements.txt

