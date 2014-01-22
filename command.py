import settings
import logging

logger = None


class Command:
    command_line = None
    room = None
    action = None
    value = None

    def __init__(self, command_line=None):
        global logger
        logger = logging.getLogger(__name__)
        self.command_line = command_line
        self.clean_command()
        self.parse_command()

    def __repr__(self):
        return "Room: %s, Action: %s, Value: %s" % (
            self.room,
            self.action,
            self.value,
        )

    def clean_command(self):
        ''' Cleans up some common errors made by the voice interpreter.

        '''
        self.command_line = self.command_line.replace('read', 'red')
        #TODO: Fix the 270 degrees test

    def parse_command(self):
        ''' Takes a line of english text and tries to interpret it
        into a command.

        '''
        line_split = self.command_line.split()

        if 'brightness' in line_split or 'dim' in line_split:
            self.action = 'dim'
            for word in line_split:
                try:
                    self.value = int(word)
                except:
                    pass

        if 'color' in line_split:
            self.action = 'hue'

        if 'temperature' in line_split:
            self.action = 'temperature'
            for word in line_split:
                try:
                    self.value = int(word)
                except:
                    pass

        for color_name in settings.COLORS.keys():
            if color_name in line_split:
                logger.debug('Found color: %s' % color_name)
                self.action = 'hue'
                self.value = settings.COLORS[color_name]

        for room_name in settings.LIGHT_GROUPS.keys():
            if room_name in line_split:
                self.room = room_name

        if 'on' in line_split:
            self.action = 'power'
            self.value = 'on'
        elif 'off' in line_split:
            self.action = 'power'
            self.value = 'off'

        if not self.room:
            logger.debug('No room specified. Assuming the whole house.')
            self.room = 'house'
