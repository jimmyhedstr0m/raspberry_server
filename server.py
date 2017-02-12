from flask import Flask, make_response, request, abort
from config_parser import ConfigParser
from ir_remote import IrRemote
from pilight_remote import PiLightRemote
from state_provider import StateProvider
import crossdomain_fix
import json

app = Flask(__name__)
config_parser = ConfigParser()


@crossdomain_fix.crossdomain(origin='*')
@app.route("/")
def hello():
    return "Hello world!"


@app.route("/status")
def status():
    return "Working fine..."


@app.route("/switches/toggle/<int:group>/<unit>", methods=["POST"])
def toggle(group, unit):
    if unit == "all":
        # print json.dumps(config_parser.get_switch_groups(), indent=2, sort_keys=True)
        switch_group = config_parser.get_switch_groups()[group]

        # for units in switch_group["units"]:

        return "Toggle all units in group " + str(group)
    else:
        try:
            unit = int(unit)
            pilight_remote = PiLightRemote(group)
            pilight_remote.execute_command(unit)
            return "Toggle group " + str(group) + " and unit " + str(unit)
        except ValueError:
            abort(400)


@app.route("/remote", methods=["POST", "OPTIONS"])
def remote():
    print json.dumps(request.json, indent=2, sort_keys=True)
    remote_id = int(request.json["remote_id"])
    command = request.json["command_id"]

    ir_remote = IrRemote(remote_id)
    ir_remote.execute_command(command)
    return(command)

if __name__ == "__main__":
    server_port = config_parser.get_server_port()
    state_provider = StateProvider()
    print json.dumps(state_provider.get_group_states(0), indent=2, sort_keys=True)
    app.run(host="0.0.0.0", port=server_port, debug=True)
