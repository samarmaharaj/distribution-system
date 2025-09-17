@echo off
ECHO Starting 3 distributed nodes...

REM Each 'start' command opens a new command prompt window
start "Node A" cmd /k "python app/app_local.py node-a 5001"
start "Node B" cmd /k "python app/app_local.py node-b 5002"
start "Node C" cmd /k "python app/app_local.py node-c 5003"

ECHO All nodes started in separate windows.
ECHO To stop the system, simply close all three new command windows.
