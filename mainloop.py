#!/usr/bin/env python

import RPi.GPIO as GPIO
import automate


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(3, GPIO.IN)
    while True:
        if GPIO.input(3):
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
