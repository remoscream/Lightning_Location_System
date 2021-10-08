""" Program for sending message to line group when raspi boot/reboot"""
import time
import requests
import LineToken

url = "https://notify-api.line.me/api/notify"
headers = {"Authorization" : "Bearer "+ LineToken.pos1}

if __name__ == '__main__':
    time.sleep(60)  # Wait for 1 minute after boot/reboot
    message = "Attention!! Raspi boot/reboot detected !"
    payload = {"message" :  message}
    r = requests.post(url, headers = headers, params=payload)
