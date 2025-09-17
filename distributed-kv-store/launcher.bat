@echo off
ECHO Starting 3 distributed nodes...

REM Change the current directory to the directory where this script is located.
REM This ensures the relative path 'app/app_local.py' works correctly.
cd /d "%~dp0"

REM Each 'start' command opens a new command prompt window
start "Node A" cmd /k "python app/app_local.py node-a 5001"
start "Node B" cmd /k "python app/app_local.py node-b 5002"
start "Node C" cmd /k "python app/app_local.py node-c 5003"

ECHO All nodes started in separate windows.
ECHO To stop the system, simply close all three new command windows.

