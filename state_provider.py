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
            data_str = json.dumps(switch_groups, indent=2)

            try:
                to_unicode = unicode
            except NameError:
                to_unicode = str

            with io.open("states.json", "w", encoding="utf8") as source_file:
                source_file.write(to_unicode(data_str))

    def get_unit_state(self, group_id, unit_id):
        return self.states[group_id]["units"][unit_id]

    def get_group_states(self, group_id):
        return self.states[group_id]["units"]

    def toggle_unit_state(self, group_id, unit_id):
        unit = self.states[group_id]["units"][unit_id]
        unit["on"] = not unit["on"]
        unit["last_event"] = str(datetime.now())

    def toggle_group_units(self, group_id, mode):
        for unit in self.states[group_id]["units"]:
            unit["on"] = mode
            unit["last_event"] = str(datetime.now())

    def toggle_all_units(self, mode=None):
        for switch_group in self.states:
            for unit in switch_group["units"]:
                if mode is not None:
                    unit["on"] = mode
                else:
                    unit["on"] = not unit["on"]

                unit["last_event"] = str(datetime.now())
