import subprocess

class TV_Remote:
    def __init__(self):
        # Create instance of config parser and load relevant config data for remote
    def execute_command(self, command_id):
        if self.validate_command(command_id):
            self._execute_command(command_id)
        else:
            print "Unknown commands, remote received following signal", arg

    def _execute_command(command_id):
        cmd = 'irsend SEND_ONCE ' + string(conf_file) + ' ' + string(command_id)
        subprocess.call(cmd, shell=True)

    def validate_command(self, command_id):
        return True # Read config.json and validate 
    
    def get_config_data(self):
        return True;
        
