class Command:
    room = None
    action = None
    value = None

    def __init__(self, room=None, action=None, value=None):
        self.room = room
        self.action = action
        self.value = value

    def __repr__(self):
        return "Room: %s, Action: %s, Value: %s" % (
            self.room,
            self.action,
            self.value,
        )

