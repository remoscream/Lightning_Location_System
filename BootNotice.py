import time
import requests
import LineToken

url = "https://notify-api.line.me/api/notify"
headers = {"Authorization" : "Bearer "+ LineToken.raspi_NiTech6Bld}

if __name__ == '__main__':
    time.sleep(60)
    message = "Attention!! Raspberry pi boot/reboot detected !"
    payload = {"message" :  message}
    r = requests.post(url, headers = headers, params=payload)

