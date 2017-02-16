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
ir_remote = IrRemote()

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
    toggle = pilight_remote.toggle_unit(group_id, unit_id)
    return succ_response(toggle)


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

    return succ_response(toggle)


# Get specific group or all groups
@app.route("/switches/group/<group_id>")
def get_group(group_id):
    if group_id == "all":
        results = StateProvider().get_all_groups()
    else:
        try:
            group = StateProvider().get_group(int(group_id))
            if group:
                return succ_response(group)
            else:
                return err_response("Unable to find group " + str(group_id))
        except ValueError:
            abort(400)


# Get specific group unit
@app.route("/switches/group/<int:group_id>/unit/<int:unit_id>")
def get_unit(group_id, unit_id):
    group = StateProvider().get_group(group_id)

    if group:
        unit = StateProvider().get_unit(group_id, unit_id)
        if unit:
            return succ_response(unit)
        else:
            err_string = "Unable to find unit " + str(unit_id)
            err_string += " in group " + str(group_id)
            return err_response(err_string)
    else:
        return err_response("Unable to find group " + str(group_id))


@app.route("/remote/<int:remote_id>/key/<key>", methods=["POST", "OPTIONS"])
def remote(remote_id, key):
    remote = ir_remote.get_remote(remote_id)

    if remote is not None:
        if str(key) in remote["keys"]:
            ir_remote.send_command(remote_id, key)

            results = {
                "remote_id": remote_id,
                "name": remote["name"],
                "key": key
            }
            return succ_response(results)
        else:
            err_string = "Key " + str(key) + " does not belong to remote " + str(remote_id)
            err_string += ", " + remote["name"]
            return err_response(err_string)
    else:
        return err_response("Unable to find remote " + str(remote_id))


@app.route("/temp")
def temp():
    temp = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("UTF-8")
    temp = float(findall("\d+\.\d+", temp)[0])
    return json.dumps({"server_temperature": temp}, indent=2, sort_keys=True, ensure_ascii=False)


def succ_response(data):
    out = {
        "results": data
    }
    return json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False)


def err_response(data):
    out = {
        "error": data
    }
    return json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False)


if __name__ == "__main__":
    server_port = config_parser.get_server_port()

    if not server_debug:
        subprocess.call("sudo service pilight start", shell=True)
        subprocess.call("sudo service pilight restart", shell=True) # fix?

    app.run(host="0.0.0.0", port=server_port, debug=server_debug)
