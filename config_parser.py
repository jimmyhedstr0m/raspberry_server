import io
import json


class ConfigParser():

    def __init__(self):
        self.load_config_file()

    def load_config_file(self):
        with io.open("config.json", "r", encoding="utf8") as data_file:
            self.config_data = json.load(data_file)

    def reload_config_file(self):
        self.load_config_file()

    def get_switch_groups(self):
        return self.config_data["switch_groups"]

    def get_switch_id(self, switch_ix):
        return self.config_data["switch_groups"][switch_ix]["remote_code"]

    def get_remote(self, remote_id):
        try:
            remote_id = int(remote_id)
            if remote_id > 0 and remote_id < len(self.config_data["ir_remotes"]):
                return self.config_data["ir_remotes"][remote_id]
            else:
                return False
        except ValueError:
            abort(400)

    def get_remote_commands(self, remote_ix):
        return self.config_data["ir_remotes"][remote_ix]["keys"]

    def get_remote_name(self, remote_ix):
        return self.config_data["ir_remotes"][remote_ix]["name"]

    def get_remote_conf_file(self, remote_ix):
        return self.config_data["ir_remotes"][remote_ix]["config_file"]

    def get_server_port(self):
        return self.config_data["server_port"]
