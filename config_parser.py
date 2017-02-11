import json


class ConfigParser

    def __init__(self):

    def load_config_file(self):
        with open("config.json") as data_file:
            self.config_data = json.load(data_file)

    def get_lamp_groups(self):

    def get_remote_commands(self, remote_id):
