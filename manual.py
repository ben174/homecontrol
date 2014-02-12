#!/usr/bin/env python

from recorder import Recorder
from control import Control
from command import Command
import time
import logging

GPIO_PIN = 3

recorder = Recorder()
#control = Control()
logger = None


def main():
    setup_logging()
    while True:
        button_press()


def button_press():
    time.sleep(1)
    command = recorder.record_command()
    print command
    #if command:
    #    control.execute_command(command)
    return
    command = Command(action='power', value='on')
    recorder.control.execute_command(command)


def setup_logging():
    # silence phue logging
    phue_log = logging.getLogger("phue")
    phue_log.setLevel(logging.WARNING)

    global logger
    logger = logging.getLogger("automate")
    logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    main()
