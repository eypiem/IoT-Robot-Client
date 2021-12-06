# IoT-Robot-Client

The goal of this project was to create an online platform in which users can find and connect to their robots from anywhere. The user can monitor the status, sensors data, and also send live commands to their robots.

The Robot is connected to an L298 motor driver which in turn runs two DC motors.
It reads a GY-80 IMU through the I2C protocol with the BMP085 temperature and pressure sensor and the ADXL345 accelerometer.
The server and the robot communicate with each other using a TCP connection.

This code is written in Python 3 and has been tested on a Raspberry Pi 3B+ running Raspberry Pi OS Lite.

## Deployment

Firstly, install [`RPi.GPIO`](https://pypi.org/project/RPi.GPIO/):

```bash
sudo apt-get update
sudo apt-get install rpi.gpio
```

To start the client:

```bash
python3 app.py
```
You can define a `systemd` daemon to start the client everytime the Raspberry Pi boots up.

## Configuration

### In `main.py`:

Set the IP address and port of the [server](https://github.com/AmirParsaMahdian/IoT-Robot-Server):
```python
TCP_IP = 'xxx.xxx.xxx.xxx'
TCP_PORT = 7070
```

Assign a name and unique ID to the robot:
```python
NAME = 'Robot X'
ID = '1as6df'
```

Configure the pinouts as you require (note that `M1_EN` and `M2_EN` need to support PWM):
```python
LED_PIN = 7
BUZZER_PIN = 8
M1_IN1 = 9
M1_IN2 = 10
M1_EN = 12
M2_IN1 = 5
M2_IN2 = 6
M2_EN = 13
```

## Authors

- [@AmirParsaMahdian](https://www.github.com/AmirParsaMahdian)


## License

[MIT](https://choosealicense.com/licenses/mit/)
