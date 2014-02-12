NEST_LOGIN = 'your@email.com'
NEST_PASS = 'password'
HUE_BRIDGE = '10.0.1.147'

COLORS = {
    'red': [0],
    'read': [0],
    'green': [25500],
    'blue': [46920],
    'rainbow': [0, 25500, 46920],
}

LIGHT_GROUPS = {
    'office': [7, 8, 9],
    'living': [6, 3, 1, 13, 15],
    'upstairs': [4, 5],
    'downstairs': [6, 3, 1, 2, 12, 7, 8, 9, 13, 15],
    'kitchen': [2],
    'bedroom': [5, 11],
    'stairs': [4, 6],
    'staircase': [4, 6],
    'hallway': [12],
    'guest': [10],
    'porch': [14],
    'house': range(1, 16),
}

DEFAULT_ROOM = 'house'

FLAC_CONVERT = 'sox audio -t wav -r 48000 -t flac audio.flac'
# or if you want to use flac command use 'flac -f audio'

AUDIO_DEVICE = 'pulse'  # omit to auto discover

RECORD_LENGTH = 3

LANGUAGE = 'en-US'

# not yet implemented
SUBSTITUTIONS = {
    'green': ['creed', 'screen'],
    'read': ['red', 'screen']
}
