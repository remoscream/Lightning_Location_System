import smbus

t_fine = 0.0  # A fine resolution temperature value over to the pressure and humidity compensation formula

digT = list(range(0, 4, 1))
digP = list(range(0, 10, 1))
digH = list(range(0, 7, 1))


def correct_signed_short(bin_value):
    """Inverse bit of signed short

    As python always read hex value as unsigned type, it's necessary to check the sign bit of the parameters which defined as signed short.

    If sign bit is 1 (minus), invert bit except sign bit and add the negative sign to decimal value (float)
    """
    if bin_value & 0x8000:
        bin_value = -(bin_value ^ 0xFFFF) + 1
    return bin_value


def compensate_temperature(adc_T):
    """Conversion of temperature from ADC (Formulas are defined in datasheet)
    """
    global t_fine
    global digT
    global digP
    global digH

    v1 = (adc_T / 16384 - digT[0] / 1024) * digT[1]
    v2 = (adc_T / 131072 - digT[0] / 8192) * (adc_T / 131072 - digT[0] / 8192) * digT[2]
    t_fine = v1 + v2  # Calculate fine resolution
    temperature = t_fine / 5120

    return temperature


def compensate_pressure(adc_P):
    """Conversion of pressure from ADC (Formulas are defined in datasheet)
    """
    global t_fine
    global digT
    global digP
    global digH

    v1 = t_fine / 2 - 64000
    v2 = v1 * v1 * digP[5] / 32768
    v2 = v2 + v1 * digP[4] * 2
    v2 = v2 / 4 + digP[3] * 65536
    v1 = (digP[2] * v1 * v1 / 524288 + digP[1] * v1) / 524288
    v1 = (1 + v1 / 32768) * digP[0]

    if v1 == 0:
        return 0  # Avoid exception caused by division by zero

    pressure = 1048576 - adc_P
    pressure = (pressure - v2 / 4096) * 6250 / v1
    v1 = digP[8] * pressure * pressure / 2147483648
    v2 = pressure * digP[7] / 32768
    pressure = pressure + (v1 + v2 + digP[6]) / 16

    return pressure


def compensate_humidity(adc_H):
    """Conversion of humidity from ADC (Formulas are defined in datasheet)
    """
    global t_fine
    global digT
    global digP
    global digH

    humidity = t_fine - 76800
    humidity = (adc_H - (digH[3] * 64 + digH[4] / 16384 * humidity)) * (
            digH[1] / 65536 * (1.0 + digH[5] / 67108864 * humidity * (1 + digH[2] / 67108864 * humidity)))
    humidity = humidity * (1.0 - digH[0] * humidity / 524288.0)
    if humidity > 100:
        humidity = 100
    elif humidity < 0:
        humidity = 0

    return humidity


class RPi_BME280:
    """A basic class used for interacting with the BME280 weather
    sensor from a Raspberry Pi over I2C"""

    def __init__(self, address, bus=1):
        self.address = address
        self.i2cbus = smbus2.SMBus(bus)

    def write_register(self, reg_address, data):
        """Write register
        """
        self.i2cbus.write_byte_data(self.address, reg_address, data)

    def get_calibration_param(self):
        """Get trimming parameters for calibrating AD result of T,P and H
        
        The trimming parameters are stored in a NVM memory in BME280
        """
        global digT
        global digP
        global digH

        calibration = []

        # Memory address : 0x88-->0x9F  (12 parameters)
        for i in range(0x88, 0x88 + 24):
            calibration.append(self.i2cbus.read_byte_data(self.address, i))

        # Memory address : 0xA1 (1 parameter)
        calibration.append(self.i2cbus.read_byte_data(self.address, 0xA1))

        # Memory address 0xE1-->0xE7 (6 parameters)
        for i in range(0xE1, 0xE1 + 7):
            calibration.append(self.i2cbus.read_byte_data(self.address, i))

        # Reconstruct bit value of trimming parameters
        # digT[0]->digT[2]: T1->T3, digP[0]->digP[8]: P1->P9, digH[0]->digH[5]: H1->H6
        digT[0] = calibration[1] << 8 | calibration[0]
        digT[1] = correct_signed_short(calibration[3] << 8 | calibration[2])
        digT[2] = correct_signed_short(calibration[5] << 8 | calibration[4])
        digP[0] = calibration[7] << 8 | calibration[6]
        digP[1] = correct_signed_short(calibration[9] << 8 | calibration[8])
        digP[2] = correct_signed_short(calibration[11] << 8 | calibration[10])
        digP[3] = correct_signed_short(calibration[13] << 8 | calibration[12])
        digP[4] = correct_signed_short(calibration[15] << 8 | calibration[14])
        digP[5] = correct_signed_short(calibration[17] << 8 | calibration[16])
        digP[6] = correct_signed_short(calibration[19] << 8 | calibration[18])
        digP[7] = correct_signed_short(calibration[21] << 8 | calibration[20])
        digP[8] = correct_signed_short(calibration[23] << 8 | calibration[22])
        digH[0] = calibration[24]
        digH[1] = correct_signed_short(calibration[26] << 8 | calibration[25])
        digH[2] = calibration[27]
        digH[3] = correct_signed_short(calibration[28] << 4 | 0x0F & calibration[29])
        digH[4] = correct_signed_short(calibration[30] << 4 | calibration[29] >> 4 & 0x0F)
        digH[5] = correct_signed_short(calibration[31])

    def general_settings(self):
        """General settings
        """
        osrs_t = 1  # Temperature oversampling x 1
        osrs_p = 1  # Pressure oversampling x 1
        osrs_h = 1  # Humidity oversampling x 1
        mode = 3  # Normal mode
        t_sb = 0  # Tstandby 0.5ms
        filter_IIR = 0  # Filter off
        spi3w_en = 0  # 3-wire SPI Disable

        ctrl_meas_reg = (osrs_t << 5) | (osrs_p << 2) | mode
        config_reg = (t_sb << 5) | (filter_IIR << 2) | spi3w_en
        ctrl_hum_reg = osrs_h

        self.write_register(0xF2, ctrl_hum_reg)
        self.write_register(0xF4, ctrl_meas_reg)
        self.write_register(0xF5, config_reg)

    def read_data(self):
        """Read data of sensors
        """
        data_sensors = []

        for i in range(0xF7, 0xF7 + 8):  # Address of registers defined in memory map in datasheet
            data_sensors.append(self.i2cbus.read_byte_data(self.address, i))
        pres_raw = (data_sensors[0] << 12) | (data_sensors[1] << 4) | (data_sensors[2] >> 4)
        temp_raw = (data_sensors[3] << 12) | (data_sensors[4] << 4) | (data_sensors[5] >> 4)
        hum_raw = (data_sensors[6] << 8) | data_sensors[7]

        temperature_trimmed = compensate_temperature(temp_raw)
        pressure_trimmed = compensate_pressure(pres_raw)
        humidity_trimmed = compensate_humidity(hum_raw)

        return temperature_trimmed, pressure_trimmed, humidity_trimmed
