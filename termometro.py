#!/usr/bin/env python3
#############################################################################
# Filename    : Thermometer.py
# Description : DIY Thermometer
# Author      : www.freenove.com
# modification: 2019/12/27
########################################################################
import RPi.GPIO as GPIO
import smbus
import time
import math

address = 0x48
bus = smbus.SMBus(1)
cmd = 0x40
ledPin = 11

def analogRead(chn):
    value = bus.read_byte_data(address, cmd + chn)
    return value


def analogWrite(value):
    bus.write_byte_data(address, cmd, value)


def setup():
    global p
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.output(ledPin, GPIO.LOW)

    p = GPIO.PWM(ledPin, 1000)
    p.start(0)


def loop():
    while True:
        value = analogRead(0)  # read ADC value A0 pin
        voltage = value / 255.0 * 3.3  # calculate voltage
        Rt = 10 * voltage / (3.3 - voltage)  # calculate resistance value of thermistor
        tempK = 1 / (1 / (273.15 + 25) + math.log(Rt / 10) / 3950.0)  # calculate temperature (Kelvin)
        tempC = tempK - 273.15  # calculate temperature (Celsius)
        p.ChangeDutyCycle(voltage)  # Convert ADC value to duty cycle of PWM
        print('ADC Value : %d, Voltage : %.2f, Temperature : %.2f' % (value, voltage, tempC))
        time.sleep(0.01)


def destroy():
    GPIO.cleanup()


if __name__ == '__main__':  # Program entrance
    print('Program is starting ... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()


