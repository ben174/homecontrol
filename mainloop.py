#!/usr/bin/env python

import RPi.GPIO as GPIO
from record import Recorder
from control import Control
from command import Command
import time
import logging

GPIO_PIN = 3

recorder = Recorder()
control = Control()
logger = None


def main():
    button_press()
    return
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN, GPIO.IN)
    while True:
        button_state = GPIO.input(GPIO_PIN)
        #print button_state
        if button_state == 0:
            button_press()


def button_press():
    time.sleep(1)
    button_state = GPIO.input(GPIO_PIN)
    # check if held down for a long time.
    if button_state == 0:
        recorder.record_command()
    else:
        command = Command(action='power', value='on')
        recorder.control.execute_command(command)


def oldmain():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(24, GPIO.IN)
    GPIO.setup(25, GPIO.OUT)
    GPIO.output(25, True)
    while True:
        print GPIO.input(24)


def setup_logging():
    # silence phue logging
    phue_log = logging.getLogger("phue")
    phue_log.setLevel(logging.WARNING)

    global logger
    logger = logging.getLogger("automate")
    logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    main()
