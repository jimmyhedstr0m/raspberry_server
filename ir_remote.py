import subprocess
from config_parser import ConfigParser
from remote_interface import Remote


class IrRemote(Remote):

    def __init__(self):
        self.config_parser = ConfigParser()
        self._max_steps = 100


    def get_remote(self, remote_id):
        return self.config_parser.get_remote(remote_id)


    def send_command(self, remote_id, key):
        remote = self.get_remote(remote_id)
        key = str(key)

        if remote:
            if key in remote["keys"]:
                cmd = "irsend SEND_ONCE " + remote["config_file"] + " " + key
                subprocess.call(cmd, shell=True)

                results = {
                    "remote_id": remote_id,
                    "name": remote["remote_name"],
                    "key": key
                }

                return Remote.succ_response(self, results)
            else:
                err_string = "Key " + str(key) + " does not belong to remote "
                err_string += str(remote_id) + " (" + remote["remote_name"] + ")"
                return Remote.err_response(self, err_string)
        else:
            return Remote.err_response(self, "Unable to find remote " + str(remote_id))


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
                        print "Send!"
                        subprocess.call(cmd, shell=True)
                else:
                    cmd += "KEY_VOLUMEDOWN"

                    for i in range(steps, 0, -1):
                        subprocess.call(cmd, shell=True)

            except ValueError:
                abort(400)
