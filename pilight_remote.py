import subprocess
from config_parser import ConfigParser


class PiLightRemote

    def __init__(self, remote_id):
        super(PiLightRemote, self).__init__(remote_id)

    def execute_command(self, command_id):
        if self.validate_command(command_id):
            self._execute_command(command_id)
        else:
            print "Unknown commands, remote received following signal", arg

    def _execute_command(command_id):
        cmd = 'pilight-send -p nexa_switch -i ' + string(self.remote_id) + ' -u ' + string(command_id)
        subprocess.call(cmd, shell=True)
