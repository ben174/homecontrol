import settings

from command import Command


class TestAutomate:
    def setup_class(self):
        pass

    def test_temperature(self):
        ''' Make sure we can set the temperature

        '''
        command_text = 'set the temperature to 80 degrees'
        command = Command(command_text)
        assert command.action == 'temperature'
        assert command.value == 80

    def test_read_correction(self):
        ''' Make sure we say 'red' when interpreter thinks 'read'

        '''
        command_text = 'set the office to read'
        command = Command(command_text)
        assert command.room == 'office'
        assert command.action == 'hue'
        assert command.value == settings.COLORS['red']

    def test_kitchen_off(self):
        ''' Make sure we can turn the kitchen off

        '''
        command_text = 'turn the kitchen off'
        command = Command(command_text)
        assert command.room == 'kitchen'
        assert command.action == 'power'
        assert command.value == 'off'

    def test_two_correction(self):
        ''' Make sure we change crazy values of '2XX' to 'to XX'

        '''
        command_text = 'set the temperature 270'
        command = Command(command_text)
        assert command.action == 'temperature'
        assert command.value == 70

    def test_green_office(self):
        ''' Make sure the office turns green

        '''
        command_text = 'make the office green'
        command = Command(command_text)
        assert command.room == 'office'
        assert command.action == 'hue'
        assert command.value == settings.COLORS['green']

    def test_blue_house(self):
        ''' Make sure the whole house turns blue

        '''
        command_text = 'turn the house blue'
        command = Command(command_text)
        assert command.room == 'house'
        assert command.action == 'hue'
        assert command.value == settings.COLORS['blue']

    def test_office_off(self):
        ''' Make sure the office lights turn off

        '''
        command_text = 'turn the office lights off'
        command = Command(command_text)
        assert command.room == 'office'
        assert command.action == 'power'
        assert command.value == 'off'

    def test_house_off(self):
        ''' Make sure the whole house turns off if we don't specify a room

        '''
        command_text = 'turn the lights off'
        command = Command(command_text)
        assert command.room == 'house'
        assert command.action == 'power'
        assert command.value == 'off'


def get_office_lights():
    ''' Gets the current state of my office lights so I know what values
    to plug in to presets.

    '''
    from phue import Bridge
    b = Bridge(settings.HUE_BRIDGE)
    b.connect()
    b.get_api()
    light_index = 9
    print b.get_light(light_index, 'on')
    print b.get_light(light_index, 'hue')
    print b.get_light(light_index, 'sat')
