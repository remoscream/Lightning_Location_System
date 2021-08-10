import time
import requests
import psutil

url = "https://notify-api.line.me/api/notify"
token = "Mw8bAvV4xesBgAk98tJvewVbLaonkxTfQP8DkXEynIq"   # raspi-Nitech6Bld
headers = {"Authorization" : "Bearer "+ token}

if __name__ == '__main__':
    try:
        message = "Attention!! Raspberry pi boot/reboot detected !"
        payload = {"message" :  message}
        r = requests.post(url, headers = headers, params=payload)
