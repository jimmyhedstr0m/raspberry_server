import subprocess
from config_parser import ConfigParser
from remote_interface import Remote


class IrRemote(Remote):

    def __init__(self, remote_id):
        super(IrRemote, self).__init(remote_id)

    def execute_command(self, command_id):
        if self.validate_command(command_id):
            self._execute_command(command_id)
        else:
            print "Unknown commands, remote received following signal", arg

    def _execute_command(command_id):
        cmd = 'irsend SEND_ONCE ' + string(conf_file) + ' ' + string(command_id)
        subprocess.call(cmd, shell=True)

