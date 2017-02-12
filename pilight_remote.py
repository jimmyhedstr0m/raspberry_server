import subprocess
from config_parser import ConfigParser


class PiLightRemote():

    def __init__(self, remote_ix):
        config_parser = ConfigParser()
        self.remote_id = config_parser.get_switch_id(remote_ix)
        self.current_status = [0, 0, 0]

    def execute_command(self, unit_id):
        # if self.validate_command(unit_id):
        self._execute_command(unit_id)
        # else:
        # print "Unknown commands, remote received following signal", arg

    def _execute_command(self, unit_id):
        print unit_id, self.current_status
        if self.current_status[unit_id] == 0:
            self.current_status[unit_id] = 1
            cmd = "pilight-send -p nexa_switch -i " + \
                str(self.remote_id) + " -u " + str(unit_id) + " -t"
        elif self.current_status[unit_id] == 1:
            self.current_status[unit_id] = 0
            cmd = "pilight-send -p nexa_switch -i " + \
                str(self.remote_id) + " -u " + str(unit_id) + " -f"
        print cmd
        subprocess.call(cmd, shell=True)
