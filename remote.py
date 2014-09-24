import sys
from control import Control
from command import Command

def main():
    print sys.argv
    arg = sys.argv[1]
    command = Command()
    command.room='living'
    command.action='power'
    command.value='on'
    if arg == '1':
    	command.value = 'on'
    elif arg == '2':
    	command.value = 'off'
    control = Control()
    control.execute_command(command)

if __name__ == '__main__':
    main()
