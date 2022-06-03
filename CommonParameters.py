"""
1. This script saves parameters that may be usually changed for convenience in LLS project
2. Please check the datasheet of AS3935 for the meaning of each parameter
3. As some parameters of BME280 are not usually changed in this project (like oversampling rate),
   please check/change them in 'RPi_BME280.py' under function 'general_settings'
"""

# Common
# The time duration per file for bme280 is calculated by SyncPeriod/TimeStep
SyncPeriod = 30       # Synchronization period for uploading to cloud, unit : second
TimeStep = 1            # Time step for saving each data point, unit : second

# as3935
add_ad3935 = 0x00       # I2C address of AS3935
bus_as3935 = 1          # Bus number of AS3935
IRQ_GPIONUM = 4         # Pin number of GPIO for IRQ in AS3935

calibration = 0x07      # Calibration number of AS3935, this value get by 'AS3935_Calibration.py'
indoor_mode = False     # Set indoor/outdoor mode, the value should be 'True' or 'False'
noise_floor = 1         # Set noise floor (0 to 7, int), this value could be auto calibrated in RPi_AS3935.py
WDTH = 1                # Set watch dog threshold (WDTH), value is between (0 to 10, int)
SREJ = 1                # Set spike rejection (SERJ), value is between (0 to 11, int)

FileAddress_as3935 = '/home/pi/Lightning_Location_System/data_as3935/'

# bme280
add_bme280 = 0x76   # I2C address of BME280
bus_bme280 = 1      # Bus number of BME280

FileAddress_bme280 = '/home/pi/Lightning_Location_System/data_bme280/'

# condition
add_condition = 0x77    # I2C address of BME280
bus_condition = 1       # Bus number of BME280

FileAddress_condition = '/home/pi/Lightning_Location_System/data_condition/'
