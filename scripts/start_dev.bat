@echo off
echo --- Starting Development Environment ---

echo Starting Frontend...
start cmd /k "cd src\frontend && npm start"

echo Starting Backend...
start cmd /k "cd src\backend && python main.py"

echo Development environment started.
echo Frontend: http://localhost:3000
echo Backend: http://localhost:5000
pause
