from control import Control
from command import Command

def main():
    command = Command()
    command.room='office'
    command.action='power'
    command.value='on'
    control = Control()
    control.execute_command(command)

if __name__ == '__main__':
    main()
