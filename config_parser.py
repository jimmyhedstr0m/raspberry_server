import json


class ConfigParser():

    def __init__(self):
        self.load_config_file()

    def load_config_file(self):
        with open("config.json") as data_file:
            self.config_data = json.load(data_file)

    def get_switch_groups(self):
        return self.config_data["switch_groups"]

    def get_remote_commands(self, remote_id):
        pass
