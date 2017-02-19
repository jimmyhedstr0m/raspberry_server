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

# Change this to False on server
server_debug = True


@crossdomain_fix.crossdomain(origin='*')
@app.route("/")
def hello():
    return "Hello world!"


@app.route("/status")
def status():
    return "Working fine..."


@app.route("/reload")
def reload():
    return "Implement server reset/reload function"


# Toggle specific group unit
@app.route("/switches/toggle/group/<int:group_id>/unit/<int:unit_id>", methods=["POST", "OPTIONS"])
def toggle(group_id, unit_id):
    return PiLightRemote().toggle_unit(group_id, unit_id)


# Set units in specific group/all groups to either on/off (1/0)
@app.route("/switches/group/<group_id>/power/<int:mode>", methods=["POST", "OPTIONS"])
def toggle_group_units(group_id, mode):
    if group_id == "all":
        return PiLightRemote().toggle_all_units(bool(mode))
    else:
        try:
            return PiLightRemote().toggle_group_units(int(group_id), bool(mode))
        except ValueError:
            abort(400)


# Get specific group or all groups
@app.route("/switches/group/<group_id>")
def get_group(group_id):
    if group_id == "all":
        return PiLightRemote().get_all_groups()
    else:
        try:
            return PiLightRemote().get_group(int(group_id))
        except ValueError:
            abort(400)


# Get specific group unit
@app.route("/switches/group/<int:group_id>/unit/<int:unit_id>")
def get_unit(group_id, unit_id):
    return PiLightRemote().get_unit(group_id, unit_id)


# Send remote signal for specific remote with lirc specified key
@app.route("/remote/<int:remote_id>/key/<key>", methods=["POST", "OPTIONS"])
def remote(remote_id, key):
    return IrRemote().send_command(remote_id, key)


# Send multiple remote signals according to a percentage value
@app.route("/remote/<int:remote_id>/volume/<mode>/<float:percentage>", methods=["POST", "OPTIONS"])
def set_volume(remote_id, mode, percentage):
    if mode == "up":
        return IrRemote().set_volume(remote_id, percentage)
    elif mode == "down":
        return IrRemote().set_volume(remote_id, -percentage)
    else:
        abort(400)


@app.route("/temp")
def temp():
    temp = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("UTF-8")
    temp = float(findall("\d+\.\d+", temp)[0])
    return json.dumps({"server_temperature": temp}, indent=2, sort_keys=True, ensure_ascii=False)


if __name__ == "__main__":
    server_port = config_parser.get_server_port()

    if not server_debug:
        subprocess.call("sudo service pilight start", shell=True)
        subprocess.call("sudo service pilight restart", shell=True) # fix?

    app.run(host="0.0.0.0", port=server_port, debug=server_debug)
