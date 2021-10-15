git -C ~/Lightning_Location_System/ pull origin main

/usr/bin/tmux new-session -d -s as3935 'python3 /home/pi/Lightning_Location_System/AS3935.py'

/usr/bin/tmux new-session -d -s bme280 'echo && python3 /home/pi/Lightning_Location_System/BME280.py'

/usr/bin/tmux new-session -d -s condition 'echo && python3 /home/pi/Lightning_Location_System/Condition.py'

/usr/bin/tmux new-session -d -s sync 'python3 /home/pi/Lightning_Location_System/AS3935_DataVerMan.py & python3 /home/pi/Lightning_Location_System/Sync.py'

