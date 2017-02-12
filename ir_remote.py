import subprocess
from config_parser import ConfigParser
from remote_interface import Remote


class IrRemote(Remote):

    def __init__(self, remote_id):
        Remote.__init__(self, remote_id)
	self.conf_file = "/etc/lirc/toshiba_tv_remote.conf"

    def execute_command(self, command_id):
        if self.validate_command(command_id):
	    print command_id
            self._execute(str(command_id))
        else:
            print "Unknown commands, remote received following signal", arg

    def _execute(self, command_id):
        cmd = "irsend SEND_ONCE " + self.conf_file + " " + str(command_id)
        subprocess.call(cmd, shell=True)
