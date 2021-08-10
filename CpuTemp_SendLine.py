import time
import requests
import psutil

url = "https://notify-api.line.me/api/notify"
token = "Mw8bAvV4xesBgAk98tJvewVbLaonkxTfQP8DkXEynIq"   # raspi-Nitech6Bld
headers = {"Authorization" : "Bearer "+ token}

if __name__ == '__main__':
    try:
        while True:
            CPUtemp = psutil.sensors_temperatures(fahrenheit=False)['cpu_thermal'][0][1]

            message = "CPU Temp: " + str('%.2f'%CPUtemp)+'°C'
            payload = {"message" :  message}
            r = requests.post(url, headers = headers, params=payload)

            time.sleep(10)

    except KeyboardInterrupt:
        print('Monitoring process broken by user...')
