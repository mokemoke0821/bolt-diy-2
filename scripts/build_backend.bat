@echo off
echo --- Building Backend ---
cd src\backend

echo Installing Python dependencies...
call python -m pip install -r requirements.txt

echo Checking Python syntax...
call python -m pylint *.py

echo Backend setup completed.
cd ..\..
pause
