@echo off
cd /d "%~dp0..\src\react"
echo --- Installing dependencies ---
call npm install
call npm install @shadcn/ui react-router-dom
pause
