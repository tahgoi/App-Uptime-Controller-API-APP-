@echo off
title Process Controller Launcher

echo [2/2] Activating venv and Starting Panel App on port 8510...
start "Panel Dashboard" cmd /k "call venv\Scripts\activate && panel serve app.py --port 8510 --allow-websocket-origin=localhost:8510 --show"

echo.
echo Both services are launching. 
echo Dashboard: http://localhost:8510
pause