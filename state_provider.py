import json
import os.path
import io
from config_parser import ConfigParser
from datetime import datetime


class StateProvider():

    def __init__(self):
        self.load_states()

    def load_states(self):
        if os.path.isfile("states.json"):
            with io.open("states.json", "r", encoding="utf8") as data_file:
                self.states = json.load(data_file)
        else:
            self.reset_states()

    def _save_states(self):
        try:
            to_unicode = unicode
        except NameError:
            to_unicode = str

        data_str = json.dumps(self.states, indent=2)
        with io.open("states.json", "w", encoding="utf8") as destination_file:
            destination_file.write(to_unicode(data_str))

    def reset_states(self):
        with io.open("config.json", "r", encoding="utf8") as data_file:
            data = json.load(data_file)
            switch_groups = data["switch_groups"]

            for switch_group in switch_groups:
                for unit in switch_group["units"]:
                    unit["on"] = False
                    unit["last_event"] = ""
                    unit["last_user"] = ""

            self.states = switch_groups
            self._save_states()

    def get_unit(self, group_id, unit_id):
        return self.states[group_id]["units"][unit_id]

    def get_group(self, group_id):
        return self.states[group_id]

    def get_all_groups(self):
        return self.states

    def toggle_unit(self, group_id, unit_id):
        unit = self.states[group_id]["units"][unit_id]
        unit["on"] = not unit["on"]
        unit["last_event"] = str(datetime.now())
        self._save_states()

    def toggle_group_units(self, group_id, mode):
        for unit in self.states[group_id]["units"]:
            unit["on"] = mode
            unit["last_event"] = str(datetime.now())

        self._save_states()

    def toggle_all_units(self, mode):
        for switch_group in self.states:
            for unit in switch_group["units"]:
                unit["on"] = mode
                unit["last_event"] = str(datetime.now())

        self._save_states()