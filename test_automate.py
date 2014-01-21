import automate
import settings


class TestAutomate:
    def setup_class(self):
        automate.setup_logging()

    def test_temperature(self):
        ''' Make sure we can set the temperature

        '''
        command_text = 'set the temperature to 80 degrees'
        command = automate.Command()
        command = automate.parse_command(command_text)
        assert command.action == 'temperature'
        assert command.value == 80

    def test_read_correction(self):
        ''' Make sure we say 'red' when interpreter thinks 'read'

        '''
        command_text = 'set the office to read'
        command = automate.Command()
        command = automate.parse_command(command_text)
        assert command.room == 'office'
        assert command.action == 'hue'
        assert command.value == settings.COLORS['red']

    def test_kitchen_off(self):
        ''' Make sure we can turn the kitchen off

        '''
        command_text = 'turn the kitchen off'
        command = automate.Command()
        command = automate.parse_command(command_text)
        assert command.room == 'kitchen'
        assert command.action == 'power'
        assert command.value == 'off'

    def test_two_correction(self):
        ''' Make sure we change crazy values of '2XX' to 'to XX'

        '''
        command_text = 'set the temperature 270'
        command = automate.Command()
        command = automate.parse_command(command_text)
        assert command.action == 'temperature'
        assert command.value == 70

    def test_green_office(self):
        ''' Make sure the office turns green

        '''
        command_text = 'make the office green'
        command = automate.Command()
        command = automate.parse_command(command_text)
        assert command.room == 'office'
        assert command.action == 'hue'
        assert command.value == settings.COLORS['green']

    def test_blue_house(self):
        ''' Make sure the whole house turns blue

        '''
        command_text = 'turn the house blue'
        command = automate.Command()
        command = automate.parse_command(command_text)
        assert command.room == 'house'
        assert command.action == 'hue'
        assert command.value == settings.COLORS['blue']

    def test_office_off(self):
        ''' Make sure the office lights turn off

        '''
        command_text = 'turn the office lights off'
        command = automate.Command()
        command = automate.parse_command(command_text)
        assert command.room == 'office'
        assert command.action == 'power'
        assert command.value == 'off'

    def test_office_off(self):
        ''' Make sure the whole house turns off if we don't specify a room

        '''
        command_text = 'turn the lights off'
        command = automate.Command()
        command = automate.parse_command(command_text)
        assert command.room == 'house'
        assert command.action == 'power'
        assert command.value == 'off'
