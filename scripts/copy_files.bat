@echo off
echo Copying necessary files to bolt-diy project...

cd ..
cd bolt-diy

rem Copy backend files
xcopy /E /I /Y "..\cipher_app\src\backend\routes" "src\backend\routes"
xcopy /E /I /Y "..\cipher_app\.env" "src\backend\.env"
xcopy /E /I /Y "..\cipher_app\src\backend\requirements.txt" "src\backend\requirements.txt"
xcopy /E /I /Y "..\cipher_app\src\backend\app.py" "src\backend\app.py"

rem Create necessary directories
mkdir src\backend\logs
mkdir config

rem Copy config files
xcopy /E /I /Y "..\cipher_app\config\development.json" "config\development.json"
xcopy /E /I /Y "..\cipher_app\config\production.json" "config\production.json"

echo Files copied successfully.
pause
