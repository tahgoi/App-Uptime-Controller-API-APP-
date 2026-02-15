@echo off
title Process Controller Launcher

echo [1/2] Activating venv and Starting API on port 8565...
start "API Engine" cmd /k "call venv\Scripts\activate && python api.py"

echo.
echo Both services are launching. 
echo API: http://localhost:8565
pause