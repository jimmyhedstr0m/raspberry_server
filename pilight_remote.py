import subprocess
from state_provider import StateProvider


class PiLightRemote():

    def __init__(self):
        self.state_provider = StateProvider()

    def toggle_unit(self, group_id, unit_id):
        switch_group = self.state_provider.get_group(group_id)
        remote_code = switch_group["remote_code"]
        cmd = "pilight-send -p nexa_switch -i " + remote_code + " -u " + str(unit_id) + " -"

        self.state_provider.toggle_unit(group_id, unit_id)
        unit = self.state_provider.get_unit(group_id, unit_id)

        if unit["on"]:
            cmd += "t"
        else:
            cmd += "f"

        subprocess.call(cmd, shell=True)
        return unit

    def toggle_group_units(self, group_id, mode):
        switch_group = self.state_provider.get_group(group_id)
        remote_code = switch_group["remote_code"]
        cmd = "pilight-send -p nexa_switch -i " + remote_code + " -a -"

        if mode:
            cmd += "t"
        else:
            cmd += "f"

        self.state_provider.toggle_group_units(group_id, mode)
        subprocess.call(cmd, shell=True)
        return self.state_provider.get_group(group_id)

    def toggle_all_units(self, mode):
        switch_groups = self.state_provider.get_all_groups()
        groups = []

        for switch_group in switch_groups:
            toggle = self.toggle_group_units(switch_group["group_id"], mode)
            groups.append(toggle)

        return groups
