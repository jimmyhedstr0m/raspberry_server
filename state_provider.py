import json
import os.path


class StateProvider():

    def __init__(self):
        self.load_states()

    def load_states(self):
        if os.path.isfile("states.json"):
            print "file exists"
        else:
            print "no file"
            file = open("states.json","w")
            file.write("")
            file.close()

        # with open("config.json") as data_file:
        #     self.config_data = json.load(data_file)

    # def reload_config_file(self):
    #     self.load_config_file()
    #
    # def get_switch_groups(self):
    #     return self.config_data["switch_groups"]
