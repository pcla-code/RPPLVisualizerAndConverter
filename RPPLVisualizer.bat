@echo off
cd /d %~dp0
start python libraries\server.py
timeout /t 2
start http://192.168.100.27:8000/pages/RPPL_LocalVisualizerCORS.html