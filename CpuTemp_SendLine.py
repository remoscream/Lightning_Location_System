import time
import requests
import psutil
import LineToken

url = "https://notify-api.line.me/api/notify"
headers = {"Authorization" : "Bearer "+ LineToken.raspi_NiTech6Bld}

if __name__ == '__main__':
    try:
        while True:
            CPUtemp = psutil.sensors_temperatures(fahrenheit=False)['cpu_thermal'][0][1]

            message = "CPU Temp: " + str('%.2f'%CPUtemp)+'°C'
            payload = {"message" :  message}
            r = requests.post(url, headers = headers, params=payload)

            time.sleep(600)

    except KeyboardInterrupt:
        print('Monitoring process broken by user...')
