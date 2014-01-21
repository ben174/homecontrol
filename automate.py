''' automate.py  - Written by Ben Friedland

    A tool to automate my house via voice commands. Accepts commands like:
        'Turn office lights on'
        'Turn upstairs lights blue'
        'Set temperature to 68'
        'Turn living room into a rainbow.'
'''

from pygsr import Pygsr
from phue import Bridge
import time
import settings


def parse_command(line):
    ''' Takes a line of english text and tries to interpret it into a command

    '''
    b = Bridge(settings.HUE_BRIDGE)
    b.connect()
    b.get_api()
    line_split = line.split()

    room = None
    command = None
    value = None

    colors = {
        'red': [0],
        'read': [0],
        'green': [25500],
        'blue': [46920],
        'rainbow': [0, 25500, 46920],
    }

    light_groups = {
        'office': [7, 8, 9],
        'living': [6, 3, 1],
        'upstairs': [4, 5],
        'kitchen': [2],
        'bedroom': [5],
        'stairs': [4, 6],
        'house': range(1, 10),
    }

    if 'brightness' in line_split:
        command = 'dim'

    if 'color' in line_split:
        command = 'hue'
        # hue colors go here

    if 'temperature' in line_split:
        command = 'temperature'
        for word in line_split:
            try:
                value = int(word)
            except:
                pass

    for color_name in colors.keys():
        if color_name in line:
            print 'found color: %s' % color_name
            command = 'hue'
            value = colors[color_name]

    for room_name in light_groups.keys():
        if room_name in line:
            room = room_name

    if 'on' in line_split:
        command = 'power'
        value = 'on'
    elif 'off' in line_split:
        command = 'power'
        value = 'off'

    print 'Command: %s' % (line)
    print 'Room: %s, Command: %s, Value: %s' % (room, command, value)

    if not (command and value):
        return False

    if not room:
        print 'You didn\'t specify a room. Assuming the whole house.'
        room = 'house'

    if command == 'power':
        light_state = (value == 'on')
        for light_index in light_groups[room]:
            print 'Setting light %s: %s' % (str(light_index), str(light_state))
            b.set_light(light_index, 'on', light_state)
            if light_state:
                # reset color
                b.set_light(light_index, 'hue', 15331)
                b.set_light(light_index, 'sat', 121)
        return True
    elif command == 'hue':
        for light_index in light_groups[room]:
            print 'Setting hue %s: %s' % (str(light_index), value[0])
            b.set_light(light_index, 'on', True)
            b.set_light(light_index, 'hue', value[0])
            b.set_light(light_index, 'sat', 255)
        return True
    elif command == 'temperature':
        if value:
            set_temperature(value)
            return True
        else:
            print 'Could not determine a temperature.'
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
    speech = Pygsr()
    speech.record(3, 1)
    result = speech.speech_to_text('en-US')
    line = result[0].lower()
    return line


def get_office_lights():
    ''' Gets the current state of my office lights so I know what values 
    to plug in to presets.

    '''
    b = Bridge(settings.HUE_BRIDGE)
    b.connect()
    b.get_api()
    light_index = 9
    print b.get_light(light_index, 'on')
    print b.get_light(light_index, 'hue')
    print b.get_light(light_index, 'sat')


if __name__ == '__main__':
    line = record_command()
    #line = 'set the office lights to red'
    parse_command(line)
