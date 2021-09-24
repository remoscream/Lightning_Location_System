from RPi_BME280 import RPi_BME280
from Get_Time import get_time
import time
import numpy as np
import psutil

sensor = RPi_BME280(address=0x77, bus=1)

sensor.general_settings()
sensor.get_calibration_param()


# Get hardware information
def get_hardware_info():
    """ Get cpu temperature('C), cpu frequency(GHz), cpu load(%) and used memory(M) per second
    """
    hardware_info = np.zeros((1, 4))
    # The temperature saved in dictionary 'cpu_thermal' --> list '0' --> tuple '0'
    hardware_info[0, 0] = psutil.sensors_temperatures(fahrenheit=False)['cpu_thermal'][0][1]
    hardware_info[0, 1] = psutil.cpu_freq(percpu=False).current / 1000  # GHz
    hardware_info[0, 2] = psutil.cpu_percent(interval=0, percpu=False)  #
    hardware_info[0, 2] = psutil.cpu_percent(interval=0, percpu=False)  # Interval should be set to 0 for a 0s delay
    hardware_info[0, 3] = psutil.virtual_memory().used / 1000 / 1000  # Mega

    return hardware_info


if __name__ == '__main__':
    try:
        hour_step = 1  # unit : hour
        second_step = 1  # unit : second

        data_num = int(hour_step * 60 * (60 / second_step))
        dataset = np.zeros((data_num, 12))

        # Main loop for sampling
        while True:
            time_now_text_terminal, time_now_text_file, time_now_int = get_time()
            # Sub loop for creating each data file
            for i in range(0, data_num, 1):
                time_now_text_terminal, time_now_text_file, time_now_int = get_time()
                dataset[i, 0:6] = time_now_int[0, 0:6]

                temperature_real, _, humidity_real = sensor.read_data()
                hardware_info = get_hardware_info()

                dataset[i, 6] = temperature_real
                dataset[i, 7] = humidity_real

                dataset[i, 8:12] = hardware_info

                print('[Box condition] : ' + time_now_text_terminal)
                print("Temperature : %6.2f C" % temperature_real)
                print("Humidity : %6.2f %%\n" % humidity_real)

                print('[Hardware info] : ')
                print("CPUtemp: %.2f°C, Freq: %.1fGHz, CPUload: %.1f%%, MemoryUsed: %.1fM\033[0K\033[6A" % (
                    dataset[i, 8], dataset[i, 9], dataset[i, 10], dataset[i, 11]))

                time.sleep(second_step)

            csv_filename = 'data_Condition_' + time_now_text_file + '.csv'
            file_address_local = '/home/pi/Lightning_Location_System/data_Condition/'
            file_address_usb = '/home/pi/Ustick/data_Condition/'

            np.savetxt(file_address_local + csv_filename, dataset, delimiter=',', fmt='%g')
            np.savetxt(file_address_usb + csv_filename, dataset, delimiter=',', fmt='%g')

    except KeyboardInterrupt:
        print('\033[0J\n' + 'Monitoring process broken by user...')
