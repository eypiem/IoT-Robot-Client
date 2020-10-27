import socket
import threading
import asyncio
import json
import time
import RPi.GPIO as GPIO
from adxl345 import ADXL345
from bmp085 import BMP085
from dc_motor import DCMotor, MotorDir

TCP_IP = '185.8.174.9'
TCP_PORT = 7070
BUFFER_SIZE = 255

NAME = 'Robot X'
ID = '1as6df'


LED_PIN = 7
BUZZER_PIN = 8
M1_IN1 = 9
M1_IN2 = 10
M1_EN = 12
M2_IN1 = 5
M2_IN2 = 6
M2_EN = 13


def pinout_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)


def receive(client, m1, m2):
    while True:
        try:
            req_json = client.recv(BUFFER_SIZE).decode('utf8')
            req_json = req_json[1:-1]
            reqs_json = req_json.split('}{')
            for req in reqs_json:
                req = '{' + req + '}'
                handle_req(req, m1, m2)
        except:
            print('Server disconnected..')
            break


def send(client):
    message_obj = {'type': 'msg', 'data': {'data': message}}
    client.sendall(json.dumps(message_obj).encode('utf-8'))


def handle_req(req_json, m1, m2):
    print(req_json)
    try:
        req = json.loads(req_json)
    except:
        return
    req_type = req['type']
    req_data = req['data']

    if req_type == 'com_led':
        if req_data['state'] is False:
            GPIO.output(LED_PIN, GPIO.LOW)
        else:
            GPIO.output(LED_PIN, GPIO.HIGH)
    elif req_type == 'com_buzzer':
        if req_data['state'] is False:
            GPIO.output(BUZZER_PIN, GPIO.LOW)
        else:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
    elif req_type == 'com_motor':
        if req_data['m1']['dir'] == 'CW':
            m1.run(MotorDir.CW, req_data['m1']['spd'])
        else:
            m1.run(MotorDir.CCW, req_data['m1']['spd'])
        if req_data['m2']['dir'] == 'CW':
            m2.run(MotorDir.CW, req_data['m2']['spd'])
        else:
            m2.run(MotorDir.CCW, req_data['m2']['spd'])


def update(client, adxl, bmp):
    try:
        while True:
            for i in range(0, 10):
                pitch, roll = adxl.read()
                message_obj = {'type': 'orientation_data', 'data': {'pitch': pitch, 'roll': roll}}
                client.sendall(json.dumps(message_obj).encode('utf-8'))
                time.sleep(.1)
            temp, press = bmp.read()
            print(f'temp: {temp} | press: {press}')
            message_obj = {'type': 'climate_data', 'data': {'temperature': temp, 'pressure': press}}
            client.sendall(json.dumps(message_obj).encode('utf-8'))
            time.sleep(.1)
    except:
        print('Error updating.')


def main():
    pinout_setup()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    adxl = ADXL345()
    adxl.init()
    bmp = BMP085()
    bmp.init()

    m1 = DCMotor(GPIO, M1_IN1, M1_IN2, M1_EN)
    m2 = DCMotor(GPIO, M2_IN1, M2_IN2, M2_EN)
    m1.setup_pins()
    m2.setup_pins()

    try:
        client.connect((TCP_IP, TCP_PORT))
        robot_json = {'type': 'self_info', 'data': {'name': NAME, 'id': ID}}
        client.sendall(json.dumps(robot_json).encode('utf-8'))

        t1 = threading.Thread(target=receive, args=(client, m1, m2))
        t2 = threading.Thread(target=update, args=(client, adxl, bmp))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    except:
        print('An error occurred!')
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
