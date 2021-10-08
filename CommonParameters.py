"""
This script saves parameters that may be usually changed for convenience in LLS project
"""

# as3935
add_ad3935 = 0x00
bus_as3935 = 1
IRQ_GPIONUM = 4

calibration = 0x07
parameter_indoor_mode = False
parameter_noise_floor = 1
parameter_WDTH = 1
parameter_SREJ = 1

FileAddress_as3935 = 'home/pi/Lightning_Location_System/data_as3935/'

# bme280
add_bme280 = 0x76
bus_bme280 = 1

FileAddress_bme280 = 'home/pi/Lightning_Location_System/data_bme280/'

# condition
add_condition = 0x77
bus_condition = 1

FileAddress_condition = 'home/pi/Lightning_Location_System/data_condition/'
