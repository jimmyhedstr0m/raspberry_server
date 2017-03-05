import subprocess
from config_parser import ConfigParser
from response_interface import Response


class IrProvider(Response):

    def __init__(self):
        self.config_parser = ConfigParser()


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
                    "key": key,
                    "value": None
                }

                return Response.succ_response(self, results)
            else:
                err_string = "Key " + str(key) + " does not belong to remote "
                err_string += str(remote_id) + " (" + remote["remote_name"] + ")"
                return Response.err_response(self, err_string)
        else:
            return Response.err_response(self, "Unable to find remote " + str(remote_id))


    def set_volume(self, remote_id, percentage):
        remote = self.get_remote(remote_id)

        if remote:
            if remote["volume_interval"]:
                steps = int(percentage * int(remote["volume_interval"]))
                cmd = "irsend SEND_ONCE " + remote["config_file"] + " "

                if percentage > 0:
                    key = "KEY_VOLUMEUP"
                    cmd += key

                    for i in range(0, steps):
                        subprocess.call(cmd, shell=True)
                else:
                    key = "KEY_VOLUMEDOWN"
                    cmd += key

                    for i in range(steps, 0, -1):
                        subprocess.call(cmd, shell=True)

                results = {
                    "remote_id": remote_id,
                    "name": remote["remote_name"],
                    "key": key,
                    "value": percentage
                }

                return Response.succ_response(self, results)
            else:
                err_string = "Missing integer 'volume_interval' for remote "
                err_string += str(remote_id) + " (" + remote["remote_name"] + ")"
                return Response.err_response(self, err_string)
        else:
            return Response.err_response(self, "Unable to find remote " + str(remote_id))
