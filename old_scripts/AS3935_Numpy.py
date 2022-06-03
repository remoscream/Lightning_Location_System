from RPi_AS3935 import RPi_AS3935
from Get_Time import get_time
import CommonParameters as cp
import RPi.GPIO as GPIO
import time
import numpy as np

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
    current_data = np.zeros([1, 9])
    reason = sensor.get_interrupt()

    time_now_text_terminal, time_now_text_file, time_now_int = get_time()

    if reason == 0x01:  # Too much noise
        sensor.raise_noise_floor()
        print(time_now_text_terminal, "Noise level too high !")
        current_data[0, 0:6] = time_now_int[0, 0:6]
        current_data[0, 6] = reason
    elif reason == 0x04:  # Disturber
        sensor.set_mask_disturber(True)
        print(time_now_text_terminal, "Disturber detected !")
        current_data[0, 0:6] = time_now_int[0, 0:6]
        current_data[0, 6] = reason
    elif reason == 0x08:  # Lightning
        distance = sensor.get_distance()
        energy = sensor.get_energy()
        print(time_now_text_terminal, "Lightning detected !", str(distance), str(energy))
        current_data[0, 0:6] = time_now_int[0, 0:6]
        current_data[0, 6] = reason
        current_data[0, 7] = distance
        current_data[0, 8] = energy

    dataset = np.concatenate((dataset, current_data), axis=0)

    # Replace data file 'data_as3935.csv' when new data comes
    # Version management will be processed by 'AS3935_DataVerMan.py'
    file_address = cp.FileAddress_as3935
    csv_filename = 'data_as3935.csv'
    np.savetxt(file_address + csv_filename, dataset, delimiter=',', fmt='%g')


# Start
dataset = np.zeros([1, 9])  # Initialize data array

# Create data file for test the cloud service
file_address = cp.FileAddress_as3935
csv_filename = 'data_as3935.csv'
np.savetxt(file_address + csv_filename, dataset, delimiter=',', fmt='%g')

GPIO.setup(cp.IRQ_GPIONUM, GPIO.IN)  # Set GPIO mode as input
GPIO.add_event_detect(cp.IRQ_GPIONUM, GPIO.RISING, callback=judge_signal) # If detect signal, judge the type

# Print first message
time_now_text_terminal, time_now_text_file, time_now_int = get_time()
print(time_now_text_terminal, "Waiting for lightning...")

try:
    while True:
        time.sleep(1)


except KeyboardInterrupt:
    print('Detecting process broken by user...')
    GPIO.remove_event_detect(cp.IRQ_GPIONUM)
    GPIO.cleanup()
