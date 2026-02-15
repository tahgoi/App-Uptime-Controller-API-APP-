@echo off
title Process Controller Launcher

echo [2/2] Activating venv and Starting Panel App on port 8589...
start "Panel Dashboard" cmd /c "call venv\Scripts\activate && panel serve app.py --port 8589 --allow-websocket-origin=* --show"

echo.
echo Both services are launching. 
echo Dashboard: http://localhost:8589
pause