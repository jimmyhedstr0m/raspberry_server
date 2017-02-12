from flask import Flask, make_response, request, abort
from config_parser import ConfigParser
from ir_remote import IrRemote
from pilight_remote import PiLightRemote
from state_provider import StateProvider
from re import findall
import crossdomain_fix
import json
import subprocess

app = Flask(__name__)
config_parser = ConfigParser()
pilight_remote = PiLightRemote()


@crossdomain_fix.crossdomain(origin='*')
@app.route("/")
def hello():
    return "Hello world!"


@app.route("/status")
def status():
    return "Working fine..."


# Toggle specific group unit
@app.route("/switches/toggle/group/<int:group_id>/unit/<int:unit_id>", methods=["POST", "OPTIONS"])
def toggle(group_id, unit_id):
    toggle = pilight_remote.toggle_unit(group_id, unit_id)
    return json.dumps({"results": toggle}, indent=2, sort_keys=True, ensure_ascii=False)


# Set units in specific group/all groups to either on/off (1/0)
@app.route("/switches/group/<group_id>/power/<int:mode>", methods=["POST", "OPTIONS"])
def toggle_group_units(group_id, mode):
    if group_id == "all":
        toggle = pilight_remote.toggle_all_units(bool(mode))
    else:
        try:
            toggle = pilight_remote.toggle_group_units(int(group_id), bool(mode))
        except ValueError:
            abort(400)

    return json.dumps({"results": toggle}, indent=2, sort_keys=True, ensure_ascii=False)


# Get specific group or all groups
@app.route("/switches/group/<group_id>")
def get_group(group_id):
    if group_id == "all":
        results = StateProvider().get_all_groups()
    else:
        try:
            results = StateProvider().get_group(int(group_id))
        except ValueError:
            abort(400)

    return json.dumps({"results": results}, indent=2, sort_keys=True, ensure_ascii=False)


# Get specific group unit
@app.route("/switches/group/<int:group_id>/unit/<int:unit_id>")
def get_unit(group_id, unit_id):
    unit = StateProvider().get_unit(group_id, unit_id)
    return json.dumps({"results": unit}, indent=2, sort_keys=True, ensure_ascii=False)


@app.route("/remote", methods=["POST", "OPTIONS"])
def remote():
    print json.dumps(request.json, indent=2, sort_keys=True)
    remote_id = int(request.json["remote_id"])
    command = request.json["command_id"]

    ir_remote = IrRemote(remote_id)
    ir_remote.execute_command(command)
    return(command)


@app.route("/temp")
def temp():
    temp = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("UTF-8")
    temp = float(findall("\d+\.\d+", temp)[0])
    return json.dumps({"server_temperature": temp}, indent=2, sort_keys=True, ensure_ascii=False)


if __name__ == "__main__":
    server_port = config_parser.get_server_port()
    #subprocess.call("sudo service pilight start", shell=True)
    # subprocess.call("sudo service pilight restart", shell=True) # fix?

    app.run(host="0.0.0.0", port=server_port, debug=True)
