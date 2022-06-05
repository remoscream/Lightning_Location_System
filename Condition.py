"""
This version use list instead of numpy for creating data

The format of data change to 4 columns as ['Time', 'Temperature', 'Humidity', 'CPUtemp']
"""

import functions_common as fun
from RPi_BME280 import RPi_BME280
import CommonParameters as cp
import time
import psutil

# Initialization
sensor = RPi_BME280(address=cp.add_condition, bus=cp.bus_condition)

sensor.general_settings()
sensor.get_calibration_param()


if __name__ == '__main__':
    try:
        data_num = int(cp.SyncPeriod / cp.TimeStep)

        # Main loop for sampling
        while True:
            dataset = []
            _, timestamp_start_sampling = fun.get_time_now()

            # Sub loop for creating each data file
            for i in range(0, data_num, 1):
                current_data = [0, 0, 0, 0]
                # Create time text
                dt_now_reformat_str, _ = fun.get_time_now()
                current_data[0] = dt_now_reformat_str

                # Read data from sensor (box temperature, box humidity, cpu temperature of raspi)
                temperature, _, humidity = sensor.read_data()
                cputemp = psutil.sensors_temperatures(fahrenheit=False)['cpu_thermal'][0][1]

                # Save data to array
                current_data[1] = temperature
                current_data[2] = humidity
                current_data[3] = cputemp

                dataset.append(current_data)

                # Print data in terminal
                print(dt_now_reformat_str)
                print("Temperature : %6.2f °C" % temperature)
                print("Humidity : %6.2f %%" % humidity)
                print("CPUtemp: %.2f °C\033[4A" % cputemp)

                time.sleep(cp.TimeStep)

            # Save data to csv file
            dataset_header = ['Time', 'Temperature', 'Humidity', 'CPUtemp']
            filename = 'data_condition_' + timestamp_start_sampling + '.csv'
            fun.save_list_to_csv(cp.FileAddress_condition + filename, dataset, dataset_header)

    except KeyboardInterrupt:
        print('\033[0J\n' + 'Monitoring process broken by user...')
