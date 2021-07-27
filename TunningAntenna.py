# Program for tunning antenna

from RPi_AS3935 import RPi_AS3935

import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)
IRQ_GPIO = 4
GPIO.setup(IRQ_GPIO, GPIO.IN)

sensor = RPi_AS3935(address=0x03, bus=1)

sensor.reset()
print('set indoors')
sensor.set_indoors(True)
print("set noise floor to 0")
sensor.set_noise_floor(0)

sensor.read_data()
print("register0x08= ", bin(sensor.registers[0x08]))
# レジスタ0x08をアンテナ共振周波数をIRQピンに出力するよう指定
sensor.set_disp_lco(True)
sensor.read_data()
print("register0x08= ", bin(sensor.registers[0x08]))

# IRQピンにマルチメータを接続し周波数を測定せよ
print("Please measure the frequency of the IRQ pin by a multi-meter")
# tune capを10秒ごとに変化させる
print("tune cap is changed every 10 seconds")
for x in range(0, 16):
    print("tun_cap= ", x)
    sensor.calibrate(tun_cap=x)
    time.sleep(10.0)

time.sleep(5.0)
# レジスタ0x08をもとに戻しておく
sensor.set_disp_lco(False)
sensor.read_data()
print("register0x08= ", bin(sensor.registers[0x08]))
