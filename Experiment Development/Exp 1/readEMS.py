from subprocess import call
import time
import requests, json
import urllib.request as urllib2
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT) #gpio18번 셋업 ->릴레이
print('setup')

#GPIO.output(17,True)

def wait_for_internet_connection():
    while True:
        try:
            response = urllib2.urlopen('http://143.248.2.25/',timeout=1)
            return
        except urllib2.URLError:
            print('urlError')
            time.sleep(15)
            pass
        except TimeoutError:
            print('TimeoutError')
            time.sleep(15)
            pass

wait_for_internet_connection()

session = requests.Session()
session.trust_env = False
headers = {'Content-Type':'application/json; charset=utf-8'}

while True:
    url = 'http://143.248.2.25:3000/getEMS'
    res = session.post(url=url, headers=headers)
    time.sleep(0.1)
    print(res.text)

    if '1' in res.text:
        GPIO.output(17,True)
        print('EMS ON')
    else:
        GPIO.output(17,False)
        print('EMS OFF')