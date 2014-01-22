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
    'living': [6, 3, 1],
    'upstairs': [4, 5],
    'kitchen': [2],
    'bedroom': [5, 11],
    'stairs': [4, 6],
    'staircase': [4, 6],
    'hallway': [12],
    'guest': [10],
    'house': range(1, 13),
}

DEFAULT_ROOM = 'house'

FLAC_CONVERT = 'sox audio -t wav -r 48000 -t flac audio.flac'
# or if you want to use flac command use 'flac -f audio'
