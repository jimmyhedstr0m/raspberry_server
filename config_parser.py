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

    def get_rooms(self):
        return self.config_data["rooms"]

    def get_remote(self, remote_id):
        try:
            remote_id = int(remote_id)
            if remote_id > -1 and remote_id < len(self.config_data["ir_remotes"]):
                return self.config_data["ir_remotes"][remote_id]
            else:
                return None
        except ValueError:
            return None;

    def get_server_port(self):
        return self.config_data["server_port"]
