#!/usr/bin/env python
''' automate.py  - Written by Ben Friedland - http://www.bugben.com

    A tool to automate my house via voice commands. Accepts commands like:
        'Turn office lights on'
        'Turn the house red.'
        'Turn upstairs lights blue.'
        'Set temperature to 68'
        'Turn living room into a rainbow.'
        'Set staircase brightness to 5.' (1-10 scale)

'''

import logging
import settings
from command import Command
from control import Control
logger = None


def record_command():
    ''' Records audio and sends it to google to translate to text

    '''
    from pygsr import Pygsr
    speech = Pygsr()
    speech.record(3)
    result = speech.speech_to_text('en-US')
    if result:
        return result[0].lower()
    return None


def get_office_lights():
    ''' Gets the current state of my office lights so I know what values
    to plug in to presets.

    '''
    from phue import Bridge
    b = Bridge(settings.HUE_BRIDGE)
    b.connect()
    b.get_api()
    light_index = 9
    logger.info(b.get_light(light_index, 'on'))
    logger.info(b.get_light(light_index, 'hue'))
    logger.info(b.get_light(light_index, 'sat'))


def setup_logging():
    # silence phue logging
    phue_log = logging.getLogger("phue")
    phue_log.setLevel(logging.WARNING)

    global logger
    logger = logging.getLogger("automate")
    logger.setLevel(logging.DEBUG)


def main():
    line = record_command()
    setup_logging()
    control = Control()
    if not line:
        logger.warn('No command recorded.')
        return
    logger.info(line)
    command = Command(line)
    logger.info(command)
    control.execute_command(command)


if __name__ == '__main__':
    main()
