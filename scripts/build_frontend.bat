@echo off
echo --- Building Frontend ---
cd src\frontend

echo Installing dependencies...
call npm install

echo Building production bundle...
call npm run build

echo Frontend build completed.
cd ..\..
pause
