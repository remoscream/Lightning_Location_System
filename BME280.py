from RPi_BME280 import RPi_BME280
from Get_Time import get_time
import time
import numpy as np

sensor = RPi_BME280(address=0x76, bus=1)

sensor.general_settings()
sensor.get_calibration_param()


if __name__ == '__main__':
    try:
        hour_step = 1  # unit : hour
        second_step = 1  # unit : second

        data_num = int(hour_step * 60 * (60 / second_step))
        dataset = np.zeros((data_num, 9))

        # Main loop for sampling
        while True:
            time_now_text_terminal, time_now_text_file, time_now_int = get_time()
            # Sub loop for creating each data file
            for i in range(0, data_num, 1):
                time_now_text_terminal, time_now_text_file, time_now_int = get_time()
                dataset[i, 0:6] = time_now_int[0, 0:6]

                temperature_real, pressure_real, humidity_real = sensor.read_data()

                dataset[i, 6] = temperature_real
                dataset[i, 7] = pressure_real / 100
                dataset[i, 8] = humidity_real

                print('[Weather now] : ' + time_now_text_terminal)
                print("Temperature : %6.2f C" % temperature_real)
                print('Pressure : %7.2f hPa' % (pressure_real / 100))
                print("Humidity : %6.2f %%\n" % humidity_real)
                time.sleep(second_step)

            csv_filename = 'data_BME280_' + time_now_text_file + '.csv'
            file_address_local = '/home/pi/Lightning_Location_System/data_BME280/'
            file_address_usb = '/home/pi/Ustick/data_BME280/'

            np.savetxt(file_address_local + csv_filename, dataset, delimiter=',', fmt='%g')
            np.savetxt(file_address_usb + csv_filename, dataset, delimiter=',', fmt='%g')

    except KeyboardInterrupt:
        print('Sampling process broken by user...')
