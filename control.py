from nest import Nest
from phue import Bridge
import settings
import logging

logger = None


class Control:
    nest = None
    bridge = None

    def __init__(self):
        global logger
        logger = logging.getLogger(__name__)
        # connect to nest
        self.nest = Nest(
            username=settings.NEST_LOGIN,
            password=settings.NEST_PASS
        )
        try:
            self.nest.login()
            self.nest.get_status()
        except:
            logger.error("Unable to connect to NEST.")
        # connect to phillips hue
        self.bridge = Bridge(
            settings.HUE_BRIDGE
        )
        try:
            self.bridge.connect()
            self.bridge.get_api()
        except:
            logger.error("Unable to connect to Hue.")

    def execute_command(self, command):
        if command.action == 'power':
            light_state = (command.value == 'on')
            for light_index in settings.LIGHT_GROUPS[command.room]:
                logger.debug('Setting light %s: %s' % (
                    str(light_index),
                    str(light_state)
                ))
                self.bridge.set_light(light_index, 'on', light_state)
                if light_state:
                    # reset color
                    self.bridge.set_light(light_index, 'hue', 15331)
                    self.bridge.set_light(light_index, 'sat', 121)
            return True
        elif command.action == 'dim':
            for light_index in settings.LIGHT_GROUPS[command.room]:
                brightness = int(255 * (command.value*0.1))
                logger.debug('Setting bright %s: %s' % (
                    str(light_index),
                    str(brightness)
                ))
                self.bridge.set_light(light_index, 'bri', brightness)
            return True
        elif command.action == 'hue':
            curr_group = settings.LIGHT_GROUPS[command.room]
            for index, light_index in enumerate(curr_group):
                # iterates over each color for fades, gradients,etc
                value = command.value[index % len(command.value)]
                logger.debug('Setting hue %s: %s' % (
                    str(light_index), value
                ))
                self.bridge.set_light(light_index, 'on', True)
                self.bridge.set_light(light_index, 'hue', value)
                self.bridge.set_light(light_index, 'sat', 255)
            return True
        elif command.action == 'temperature':
            if command.value:
                self.nest.set_temperature(command.value)
                return True
            else:
                logger.error('Could not determine a temperature.')
        return False
