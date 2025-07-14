#!/bin/bash

echo "Stopping running FastAPI app..."

# Find and kill the process running main.py (or uvicorn/gunicorn)
APP_PID=$(ps aux | grep 'main.py' | grep -v grep | awk '{print $2}')

if [ -z "$APP_PID" ]; then
  echo "No FastAPI app is currently running."
else
  echo "Killing process ID $APP_PID"
  kill -9 $APP_PID
fi

echo "Cleaning up application directory..."

if [ -d "/home/ubuntu/prodapp" ]; then
  if [ "$PWD" = "/home/ubuntu/prodapp" ]; then
    echo "Current directory is /home/ubuntu/prodapp, proceeding with cleanup."
    cd .. || exit 1
  else
    echo "Current directory is not /home/ubuntu/prodapp, exiting."
  fi

  sudo rm -rf /home/ubuntu/*
  sudo rm -rf /opt/codedeploy-agent/deployment-root/*
  exit 1
else
  echo "Application directory does not exist."
  exit 0
fi