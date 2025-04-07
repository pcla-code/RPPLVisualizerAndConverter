@echo off
cd /d %~dp0

:: Start their local server to get their username
start python server.py

:: Wait 2 seconds to ensure the server is running
timeout /t 2

:: Open the visualizer hosted on your machine (Neithan's PC)
start microsoft-edge:http://192.168.100.27:8000/pages/RPPL_LocalVisualizerCORS.html
