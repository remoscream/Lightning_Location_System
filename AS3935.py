"""
This version use list instead of numpy for creating data

The format of data change to 3 columns as ['Time', 'Marker', 'Distance']
(Use string time and delete energy)
"""

import functions_common as fun
from RPi_AS3935 import RPi_AS3935
import CommonParameters as cp
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Initialization
sensor = RPi_AS3935(address=cp.add_ad3935, bus=cp.bus_as3935)
sensor.calibrate(tun_cap=cp.calibration)  # Adjust tuning capacitor
sensor.reset()
sensor.set_indoors(cp.indoor_mode)
sensor.set_noise_floor(cp.noise_floor)
sensor.set_WDTH(cp.WDTH)
sensor.set_SREJ(cp.SREJ)


# Judge the signal to interrupt the IRQ
def judge_signal(self):
    time.sleep(0.003)
    global sensor
    global dataset
    global dataset_header

    current_data = [0, 0, 0]  # Initialize data array (list)

    reason = sensor.get_interrupt()

    dt_now_reformat, _ = fun.get_time_now()

    if reason == 0x01:  # Too much noise
        sensor.raise_noise_floor()
        print(dt_now_reformat, "Noise level too high !")
        current_data[0] = dt_now_reformat
        current_data[1] = 'noise'
    elif reason == 0x04:  # Disturber
        sensor.set_mask_disturber(True)
        print(dt_now_reformat, "Disturber detected !")
        current_data[0] = dt_now_reformat
        current_data[1] = 'disturber'
    elif reason == 0x08:  # Lightning
        distance = sensor.get_distance()
        energy = sensor.get_energy()
        print(dt_now_reformat, "Lightning detected ! Distance:", str(distance))
        current_data[0] = dt_now_reformat
        current_data[1] = 'lightning'
        current_data[2] = distance

    dataset.append(current_data)

    # Replace data file 'data_as3935.csv' when new data comes
    # Version management will be processed by 'AS3935_DataVerMan.py'

    fun.save_list_to_csv(cp.FileAddress_as3935 + 'data_as3935.csv', dataset, dataset_header)


# Start
dataset = []  # Initialize data array
dataset_header = ['Time', 'Marker', 'Distance']

# Create data file for test the cloud service
fun.save_list_to_csv(cp.FileAddress_as3935 + 'data_as3935.csv', dataset, dataset_header)

GPIO.setup(cp.IRQ_GPIONUM, GPIO.IN)  # Set GPIO mode as input
GPIO.add_event_detect(cp.IRQ_GPIONUM, GPIO.RISING, callback=judge_signal)  # Judge

dt_now_reformat, _ = fun.get_time_now()
print(dt_now_reformat, "Waiting for lightning...")

try:
    while True:
        time.sleep(1)


except KeyboardInterrupt:
    print('Detecting process broken by user...')
    GPIO.remove_event_detect(cp.IRQ_GPIONUM)
    GPIO.cleanup()
