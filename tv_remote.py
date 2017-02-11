import subprocess
from config_parser import ConfigParser


class TvRemote:

    def __init__(self, remote_id):
        self.remote_id = remote_id
        self.config = ConfigParser()
        self.remote_commands = self.config.get_remote_commands()

    def execute_command(self, command_id):
        if self.validate_command(command_id):
            self._execute_command(command_id)
        else:
            print "Unknown commands, remote received following signal", arg

    def _execute_command(command_id):
        cmd = 'irsend SEND_ONCE ' + string(conf_file) + ' ' + string(command_id)
        subprocess.call(cmd, shell=True)

    def validate_command(self, command_id):
        return command_id in self.remote_commands
