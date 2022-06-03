"""
This version use list instead of numpy for creating data

The format of data change to 4 columns as ['Time', 'Temperature', 'Pressure', 'Humidity']
"""

import functions_common as fun
from RPi_BME280 import RPi_BME280
import CommonParameters as cp
import time


# from Get_Time import get_time
# import numpy as np

# Initialization
sensor = RPi_BME280(address=cp.add_bme280, bus=cp.bus_bme280)

sensor.general_settings()
sensor.get_calibration_param()


if __name__ == '__main__':
    try:
        data_num = int(cp.SyncPeriod / cp.TimeStep)

        # Sampling
        while True:
            dataset = []
            current_data = [0, 0, 0, 0]

            _, dt_now_reformat_int = fun.get_time_now()

            # Sub loop for creating each data file
            for i in range(0, data_num, 1):
                # Create time text
                # time_now_text_terminal, time_now_text_file, time_now_int = get_time()
                dt_now_reformat_str, _ = fun.get_time_now()
                current_data[0] = dt_now_reformat_str

                # Read data from sensor
                temperature, pressure, humidity = sensor.read_data()

                # Save data to array
                current_data[1] = temperature
                current_data[2] = pressure / 100
                current_data[3] = humidity

                dataset.append(current_data)

                # Print data in terminal
                print('\n' + dt_now_reformat_str)
                print("Temperature : %6.2f °C" % temperature)
                print('Pressure : %7.2f hPa' % (pressure / 100))
                print("Humidity : %6.2f %%\033[4A" % humidity)  # '\033[4A' for display data at first position

                time.sleep(cp.TimeStep)

            # Save data to csv file
            dataset_header = ['Time', 'Temperature', 'Pressure', 'Humidity']
            filename = 'data_bme280_' + dt_now_reformat_int + '.csv'
            fun.save_list_to_csv(cp.FileAddress_bme280 + filename, dataset, dataset_header)

    except KeyboardInterrupt:
        print('\033[0J\n' + 'Sampling process broken by user...')
