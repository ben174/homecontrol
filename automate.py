from pygsr import Pygsr
from phue import Bridge
import time

if __name__ == '__main__':
    b = Bridge('10.0.1.147')
    b.connect()
    b.get_api()
    speech = Pygsr()
    speech.record(3, 1)
    result = speech.speech_to_text('en-US') 
    line = result[0]

    room = None
    command = None
    value = None

    light_groups = {
        'office': [7,8,9],
        'living': [6,3,1],
        'upstairs': [4,5],
        'kitchen': [2],
        'bedroom': [5],
        'stairs': [4,6],
        'house': range(1,9),
    }

    if 'brightness' in line:
        command = 'dim'

    if 'color' in line:
        command = 'hue'
        # hue colors go here

    if 'office' in line:
        room = 'office'
    elif 'living' in line:
        room = 'living'
    elif 'upstairs' in line:
        room = 'upstairs'
    elif 'bedroom' in line:
        room = 'bedroom'
    elif 'kitchen' in line:
        room = 'kitchen'
    elif 'stairs' in line:
        room = 'stairs'

    if 'on' in line:
        command = 'power'
        value = 'on'
    elif 'off' in line:
        command = 'power'
        value = 'off'


    print 'Room: %s, Command: %s, Value: %s' % (room, command, value)

    if not (room and command and value):
        print 'not enough info'


    if command == 'power':
        light_state = (value == 'on')
        for light_index in light_groups[room]:
            print 'Setting light %s: %s' % (str(light_index), str(light_state))
            b.set_light(light_index,'on', light_state)



