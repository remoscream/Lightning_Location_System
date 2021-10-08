"""
Program for tuning the antenna of AS3935
"""

from RPi_AS3935 import RPi_AS3935
import RPi.GPIO as GPIO
import CommonParameters as cp
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(cp.IRQ_GPIONUM, GPIO.IN)  # Set GPIO mode as input

sensor = RPi_AS3935(address=cp.add_ad3935, bus=cp.bus_as3935)

# Set mode and noise floor for calibrating
sensor.reset()
print('set indoors')
sensor.set_indoors(True)
print("set noise floor to 0")
sensor.set_noise_floor(0)


sensor.read_data()
print("register0x08= ", bin(sensor.registers[0x08]))

# Set IRQ pin for output the waveform resonate signal
sensor.set_disp_lco(True)
sensor.read_data()
print("register0x08= ", bin(sensor.registers[0x08]))

# User should use oscilloscope or other meters to measure the resonate frequency of the signal from IRQ
print("Please measure the frequency of the IRQ pin by a multi-meter")
print("tune cap is changed every 10 seconds")
for x in range(0, 16):
    print("tun_cap= ", x)
    sensor.calibrate(tun_cap=x)
    time.sleep(10.0)

# Return to the default value
sensor.set_disp_lco(False)
sensor.read_data()
print("register0x08= ", bin(sensor.registers[0x08]))
