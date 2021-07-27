import time
import shutil
import subprocess
from datetime import datetime

gdrive_foldername = 'raspi-kasugai'

datapath_AS3935 = 'Lightning_Location_System_Data/' + gdrive_foldername + '/data_AS3935'
datapath_BME280 = 'Lightning_Location_System_Data/' + gdrive_foldername + '/data_BME280'
datapath_Condition = 'Lightning_Location_System_Data/' + gdrive_foldername + '/data_Condition'

# Get hour (now)
def get_time():
    dt_now = datetime.now()
    time_now_hour = int(dt_now.strftime("%H"))
    time_now_minute = int(dt_now.strftime("%M"))

    return time_now_hour,time_now_minute

# Synchronize after first run
subprocess.run('rclone sync /home/pi/Lightning_Location_System/data_AS3935 gdrive:' + datapath_AS3935, shell=True, encoding='utf-8', stdout=subprocess.PIPE)

subprocess.run('rclone sync /home/pi/Lightning_Location_System/data_BME280 gdrive:' + datapath_BME280, shell=True, encoding='utf-8', stdout=subprocess.PIPE)

subprocess.run('rclone sync /home/pi/Lightning_Location_System/data_Condition gdrive:' + datapath_Condition, shell=True, encoding='utf-8', stdout=subprocess.PIPE)


while True:
    time.sleep(30)
    hour_now,minute_now = get_time()
    if hour_now % 5 == 0 and minute_now % 30 == 0 : # Synchronize per 5h30m
        subprocess.run('rclone sync /home/pi/Lightning_Location_System/data_AS3935 gdrive:' + datapath_AS3935, shell=True, encoding='utf-8', stdout=subprocess.PIPE)

        subprocess.run('rclone sync /home/pi/Lightning_Location_System/data_BME280 gdrive:' + datapath_BME280, shell=True, encoding='utf-8', stdout=subprocess.PIPE)

        subprocess.run('rclone sync /home/pi/Lightning_Location_System/data_Condition gdrive:' + datapath_Condition, shell=True, encoding='utf-8', stdout=subprocess.PIPE)

