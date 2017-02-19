import subprocess
from state_provider import StateProvider
from remote_interface import Remote


class PiLightRemote(Remote):

    def __init__(self):
        self.base = "pilight-send -p nexa_switch -i "
        self.state_provider = StateProvider()


    def _send_group_command(self, group, mode):
        remote_code = group["remote_code"]
        cmd = self.base + remote_code + " -a -"

        self.state_provider.toggle_group_units(group["group_id"], mode)

        if mode:
            cmd += "t"
        else:
            cmd += "f"

        subprocess.call(cmd, shell=True)


    def get_unit(self, group_id, unit_id):
        switch_group = self.state_provider.get_group(group_id)

        if switch_group:
            unit = self.state_provider.get_unit(group_id, unit_id)

            if unit:
                return Remote.succ_response(self, unit)
            else:
                err_string = "Unable to find unit " + str(unit_id)
                err_string += " in group " + str(group_id)
                return Remote.err_response(self, err_string)
        else:
            return Remote.err_response(self, "Unable to find group " + str(group_id))


    def get_group(self, group_id):
        switch_group = self.state_provider.get_group(group_id)

        if switch_group:
            return Remote.succ_response(self, switch_group)
        else:
            return Remote.err_response(self, "Unable to find group " + str(group_id))


    def get_all_groups(self):
        switch_groups = self.state_provider.get_all_groups()

        if len(switch_groups) > 0:
            return Remote.succ_response(self, switch_groups)
        else:
            return Remote.err_response(self, "Unable to find any groups in config.json")


    def toggle_unit(self, group_id, unit_id):
        switch_group = self.state_provider.get_group(group_id)

        if switch_group:
            unit = self.state_provider.get_unit(group_id, unit_id)

            if unit:
                remote_code = switch_group["remote_code"]
                cmd = self.base + remote_code + " -u " + str(unit_id) + " -"

                self.state_provider.toggle_unit(group_id, unit_id)
                unit = self.state_provider.get_unit(group_id, unit_id)

                if unit["power_on"]:
                    cmd += "t"
                else:
                    cmd += "f"

                subprocess.call(cmd, shell=True)
                return Remote.succ_response(self, unit)
            else:
                err_string = "Unable to find unit " + str(unit_id)
                err_string += " in group " + str(group_id)
                return Remote.err_response(self, err_string)
        else:
            return Remote.err_response(self, "Unable to find group " + str(group_id))


    def toggle_group_units(self, group_id, mode):
        switch_group = self.state_provider.get_group(group_id)

        if switch_group:
            self._send_group_command(switch_group, mode)
            return Remote.succ_response(self, switch_group)
        else:
            return Remote.err_response(self, "Unable to find group " + str(group_id))


    def toggle_all_units(self, mode):
        switch_groups = self.state_provider.get_all_groups()

        for switch_group in switch_groups:
            self._send_group_command(switch_group, mode)

        return self.get_all_groups()
