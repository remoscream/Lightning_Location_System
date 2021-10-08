from RPi_BME280 import RPi_BME280
from Get_Time import get_time
import CommonParameters as cp
import time
import numpy as np
import psutil

# Initialization
sensor = RPi_BME280(address=cp.add_condition, bus=cp.bus_condition)

sensor.general_settings()
sensor.get_calibration_param()


if __name__ == '__main__':
    try:
        data_num = int(cp.SyncPeriod / cp.TimeStep)
        dataset = np.zeros((data_num, 9))

        # Main loop for sampling
        while True:
            time_now_text_terminal, time_now_text_file, time_now_int = get_time()
            # Sub loop for creating each data file
            for i in range(0, data_num, 1):
                # Create time text
                time_now_text_terminal, time_now_text_file, time_now_int = get_time()
                dataset[i, 0:6] = time_now_int[0, 0:6]

                # Read data from sensor (box temperature, box humidity, cpu temperature of raspi)
                temperature, _, humidity = sensor.read_data()
                cputemp = psutil.sensors_temperatures(fahrenheit=False)['cpu_thermal'][0][1]

                # Save data to array
                dataset[i, 6] = temperature
                dataset[i, 7] = humidity
                dataset[i, 8] = cputemp

                # Print data in terminal
                print('[Box condition] : ' + time_now_text_terminal)
                print("Temperature : %6.2f °C" % temperature)
                print("Humidity : %6.2f %%\n" % humidity)
                print("CPUtemp: %.2f °C\033[4A" % cputemp)

                time.sleep(cp.TimeStep)

            # Save data to csv file
            csv_filename = 'data_condition_' + time_now_text_file + '.csv'
            file_address_local = cp.FileAddress_condition

            np.savetxt(file_address_local + csv_filename, dataset, delimiter=',', fmt='%g')

    except KeyboardInterrupt:
        print('\033[0J\n' + 'Monitoring process broken by user...')
