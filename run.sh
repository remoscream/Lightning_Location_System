#!/bin/bash

tmux new-session -d -s AS3935 'python3 /home/pi/Lightning_Location_System/AS3935.py'

tmux new-session -d -s BME280 'echo && python3 /home/pi/Lightning_Location_System/BME280.py'

tmux new-session -d -s Condition 'echo && python3 /home/pi/Lightning_Location_System/Condition.py'

tmux new-session -d -s Sync 'python3 /home/pi/Lightning_Location_System/VerMan_AS3935.py & python3 /home/pi/Lightning_Location_System/Sync.py'
