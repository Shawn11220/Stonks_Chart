#!/bin/bash
echo "Starting installation script..."
cd /home/ubuntu/prodapp || exit 1

echo "Installing dependencies..."
sudo apt-get update
sudo apt-get install python3-pip python3-venv python3-full -y

echo "Setting up Python virtual environment..."
python3 -m venv /home/ubuntu/prodapp/venv
# if [ ! -d "venv" ]; then
#   echo "Creating virtual environment..."
#   python3 -m venv venv
# fi

if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment."
    exit 1
fi

echo "Activating virtual environment..."
source /home/ubuntu/prodapp/venv/bin/activate

echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

