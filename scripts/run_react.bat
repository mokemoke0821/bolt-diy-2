@echo off
cd /d "%~dp0..\src\react"
echo --- Starting React App ---
call npm run dev -- --host
pause
