import subprocess
from config_parser import ConfigParser


class IrRemote():

    def __init__(self):
        self.config_parser = ConfigParser()
        self._max_steps = 80

    def send_command(self, remote_id, key):
        remote = self.config_parser.get_remote(remote_id)
        key = str(key)

        if remote and key in remote["keys"]:
            cmd = "irsend SEND_ONCE " + remote["config_file"] + " " + key
            subprocess.call(cmd, shell=True)
            return True
        else:
            return False

    def set_volume(self, remote_id, percentage):
        remote = self.config_parser.get_remote(remote_id)

        if remote:
            try:
                value = float(percentage) * 100.0
                steps = value * self._max_steps
                cmd = "irsend SEND_ONCE " + remote["config_file"] + " "

                if value > 0:
                    cmd += "KEY_VOLUMEUP"

                    for i in range(0, steps):
                        subprocess.call(cmd, shell=True)
                else:
                    cmd += "KEY_VOLUMEDOWN"

                    for i in range(steps, 0, -1):
                        subprocess.call(cmd, shell=True)

            except ValueError:
                abort(400)
