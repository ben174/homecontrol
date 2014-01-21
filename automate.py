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
logger = None


class Command:
    room = None
    action = None
    value = None

    def __init__(self, room=None, action=None, value=None):
        self.room = room
        self.action = action
        self.value = value

    def __repr__(self):
        return "Room: %s, Action: %s, Value: %s" % (
            self.room,
            self.action,
            self.value,
        )


def clean_command(line):
    ''' Cleans up some common errors made by the voice interpreter.

    '''
    line = line.replace('read', 'red')
    return line


def parse_command(line):
    ''' Takes a line of english text and tries to interpret it into a command

    '''
    line_split = line.split()

    command = Command()


    if 'brightness' in line_split or 'dim' in line_split:
        command.action = 'dim'
        for word in line_split:
            try:
                command.value = int(word)
            except:
                pass

    if 'color' in line_split:
        command.action = 'hue'
        # hue colors go here

    if 'temperature' in line_split:
        command.action = 'temperature'
        for word in line_split:
            try:
                command.value = int(word)
            except:
                pass

    for color_name in settings.COLORS.keys():
        if color_name in line:
            logger.debug('Found color: %s' % color_name)
            command.action = 'hue'
            command.value = settings.COLORS[color_name]

    for room_name in settings.LIGHT_GROUPS.keys():
        if room_name in line:
            command.room = room_name

    if 'on' in line_split:
        command.action = 'power'
        command.value = 'on'
    elif 'off' in line_split:
        command.action = 'power'
        command.value = 'off'

    #logger.info('Command: %s' % (line))
    #logger.debug('Room: %s, Command: %s, Value: %s' % (room, command, value))

    if not command.room:
        logger.debug('You didn\'t specify a room. Assuming the whole house.')
        command.room = 'house'

    return command



def execute_command(command):
    print 'Comamnd: %s' % str(command)
    from phue import Bridge
    b = Bridge(settings.HUE_BRIDGE)
    b.connect()
    b.get_api()
    if command.action == 'power':
        light_state = (command.value == 'on')
        for light_index in settings.LIGHT_GROUPS[command.room]:
            logger.debug('Setting light %s: %s' % (
                str(light_index),
                str(light_state)
            ))
            b.set_light(light_index, 'on', light_state)
            if light_state:
                # reset color
                b.set_light(light_index, 'hue', 15331)
                b.set_light(light_index, 'sat', 121)
        return True
    elif command.action == 'dim':
        for light_index in settings.LIGHT_GROUPS[command.room]:
            brightness = int(255 * (command.value*0.1))
            logger.debug('Setting bright %s: %s' % (
                str(light_index),
                str(brightness)
            ))
            b.set_light(light_index, 'bri', brightness)
        return True
    elif command.action == 'hue':
        curr_group = settings.LIGHT_GROUPS[command.room]
        for index, light_index in enumerate(curr_group):
            # iterates over each color for fades, gradients,etc
            value = command.value[index % len(command.value)]
            logger.debug('Setting hue %s: %s' % (
                str(light_index), value
            ))
            b.set_light(light_index, 'on', True)
            b.set_light(light_index, 'hue', value)
            b.set_light(light_index, 'sat', 255)
        return True
    elif command.action == 'temperature':
        if value:
            set_temperature(command.value)
            return True
        else:
            logger.error('Could not determine a temperature.')
    return False


def set_temperature(degrees):
    ''' Sets temperature of nest thermostat to specified degrees.

    '''
    from nest import Nest
    nest = Nest(username=settings.NEST_LOGIN, password=settings.NEST_PASS)
    nest.login()
    nest.get_status()
    nest.set_temperature(degrees)


def record_command():
    ''' Records audio and sends it to google to translate to text

    '''
    from pygsr import Pygsr
    speech = Pygsr()
    speech.record(3, 1)
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
    #logging.basicConfig(filename='automate.log',level=logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')


def main():
    setup_logging()
    #line = record_command()
    line = 'set living room brightness to 5'
    if not line:
        logger.warn('No command recorded.')
        return
    command = parse_command(line)
    execute_command(command)


if __name__ == '__main__':
    main()
