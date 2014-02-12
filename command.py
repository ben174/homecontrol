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
        clean_output = self.command_line
        clean_output = clean_output.replace('read', 'red')
        clean_output = clean_output.replace('creed', 'green')
        clean_output = clean_output.replace('screen', 'green')
        clean_output = clean_output.replace('cream', 'green')
        #[sub for sub in settings.SUBSTITUTIONS if sub in words]
        if clean_output != self.command_line:
            logger.info("I heard: %s" % self.command_line)
            logger.info("But I corrected it to: %s" % clean_output)
        self.command = clean_output
        #TODO: Fix the 270 degrees test

    def parse_command(self):
        ''' Takes a line of english text and tries to interpret it
        into a command.

        '''
        words = self.command_line.split()

        if 'brightness' in words or 'dim' in words:
            self.action = 'dim'
            for word in words:
                try:
                    self.value = int(word)
                except:
                    pass

        if 'color' in words:
            self.action = 'hue'

        if 'temperature' in words:
            self.action = 'temperature'
            for word in words:
                try:
                    self.value = int(word)
                except:
                    pass

        for color_name in settings.COLORS.keys():
            if color_name in words:
                logger.debug('Found color: %s' % color_name)
                self.action = 'hue'
                self.value = settings.COLORS[color_name]

        for room_name in settings.LIGHT_GROUPS.keys():
            if room_name in words:
                self.room = room_name

        if 'on' in words:
            self.action = 'power'
            self.value = 'on'
        elif 'off' in words:
            self.action = 'power'
            self.value = 'off'

        if not self.room:
            self.room = settings.DEFAULT_ROOM
