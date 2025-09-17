#!/bin/bash
echo "Starting 3 distributed nodes..."

# The '&' runs each command in the background
python3 app/app_local.py node-a 5001 &
python3 app/app_local.py node-b 5002 &
python3 app/app_local.py node-c 5003 &

echo "All nodes started as background processes."
echo "To see logs, you would typically redirect output to files."
echo "To stop the system, run: 'pkill -f app_local.py'"
