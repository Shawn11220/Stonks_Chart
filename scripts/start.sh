#!bin/bash
echo "Starting the application..."

source /home/ubuntu/prodapp/venv/bin/activate

nohup uvicorn main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
echo "Application started. Logs are being written to app.log."