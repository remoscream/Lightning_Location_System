import time
import shutil
from datetime import datetime


# Get hour (now)
def get_hour():
    dt_now = datetime.now()
    time_now_hour = int(dt_now.strftime("%H"))

    return time_now_hour


# Get time text (now)
def get_time_text():
    dt_now = datetime.now()
    time_now_text = dt_now.strftime("%m-%d-%H-%M-%S")

    return time_now_text


file_address_local = '/home/pi/Lightning_Location_System/data_AS3935/'
file_address_usb = '/home/pi/Ustick/data_AS3935/'

filename_old = 'data_AS3935.csv'
hour_old = get_hour()

while True:
    time.sleep(1)
    hour_now = get_hour()
    if hour_now - hour_old != 0:
        hour_old = hour_now
        time_text = get_time_text()
        filename_new = 'data_AS3935_' + time_text + '.csv'
        shutil.copy(file_address_local + filename_old, file_address_local + filename_new)
        shutil.copy(file_address_local + filename_old, file_address_usb + filename_new)
