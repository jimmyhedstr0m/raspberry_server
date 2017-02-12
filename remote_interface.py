from config_parser import ConfigParser


class Remote():

    def __init__(self, remote_id):
        self.remote_id = remote_id
        self.config = ConfigParser()
        self.remote_commands = self.config.get_remote_commands(remote_id)

    def execute_command(self, command_id):
        raise NotImplementedError("This is only an interface")

    def validate_command(self, command_id):
        return command_id in self.remote_commands
