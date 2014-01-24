#!/usr/bin/env python

import RPi.GPIO as GPIO
import automate

GPIO_PIN = 3


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN, GPIO.IN)
    while True:
        button_state = GPIO.input(GPIO_PIN)
        #print button_state
        if button_state == 0:
            automate.main()

def oldmain():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(24, GPIO.IN)
    GPIO.setup(25, GPIO.OUT)
    GPIO.output(25, True)
    while True:
        print GPIO.input(24)

if __name__ == '__main__':
    main()
