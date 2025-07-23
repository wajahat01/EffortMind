#!/bin/bash

# Start EffortMind: Backend and Frontend

# Start backend
cd backend
pip install -r requirements.txt
python app.py &
BACKEND_PID=$!
cd ..

echo "Backend started with PID $BACKEND_PID."

# Start frontend
cd frontend
npm install
npm start 