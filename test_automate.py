import automate


class TestAutomate:
    def setup_class(self):
        automate.setup_logging()

    def test_temperature(self):
        command_text = 'set the temperature to 80 degrees'
        command = automate.Command()
        command = automate.parse_command(command_text)
        assert command.action == 'temperature'
        assert command.value == 80

    def test_green_office(self):
        command_text = 'make the office green'
        command = automate.Command()
        command = automate.parse_command(command_text)
        assert command.room == 'office'
        assert command.action == 'hue'
        assert command.value == [25500]

    def test_blue_house(self):
        command_text = 'turn the house blue'
        command = automate.Command()
        command = automate.parse_command(command_text)
        assert command.room == 'house'
        assert command.action == 'hue'
        assert command.value == [46920]

    def test_office_off(self):
        command_text = 'turn the office lights off'
        command = automate.Command()
        command = automate.parse_command(command_text)
        assert command.room == 'office'
        assert command.action == 'power'
        assert command.value == 'off'
