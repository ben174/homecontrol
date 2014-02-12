from command import Command
import logging
import settings
from pygsr import Pygsr

logger = None


class Recorder:
    def __init__(self):
        global logger
        logger = logging.getLogger(__name__)
        self.speech = Pygsr()

    def record_command(self):
        ''' Records audio and sends it to google to translate to text.

        '''
        self.speech.record(settings.RECORD_LENGTH)
        result = self.speech.speech_to_text()
        line = None
        if result:
            line = result[0].lower()
        if not line:
            logger.warn('No command recorded.')
            return None
        logger.info(line)
        command = Command(line)
        logger.info(command)
        return command
