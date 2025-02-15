@echo off
echo --- Deploying Backend to Production ---

cd src\backend

echo Installing production dependencies...
call python -m pip install -r requirements.txt

echo Setting up environment...
copy ..\..\config\production.json config.json
copy ..\..\.env .env

echo Starting Gunicorn server...
call gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:create_app()

echo Backend deployment completed.
cd ..\..
pause
