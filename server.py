from flask import Flask, make_response, request, abort
from config_parser import ConfigParser
from ir_provider import IrProvider
from light_provider import LightProvider
from re import findall
import crossdomain_fix
import json
import subprocess

app = Flask(__name__)
config_parser = ConfigParser()
light_provider = LightProvider()
ir_provider = IrProvider()

# Change this to False on server
server_debug = False


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


# Get all rooms
@app.route("/rooms")
def get_rooms():
    return light_provider.get_all_rooms()


# Get specific room
@app.route("/room/<int:room_id>")
def get_room(room_id):
    return light_provider.get_room(room_id)


# Get specific unit in specific room
@app.route("/room/<int:room_id>/unit/<string:unit_id>")
def get_room_unit(room_id, unit_id):
    return light_provider.get_room_unit(room_id, unit_id)


# Toggle specific room
@app.route("/toggle/room/<int:room_id>", methods=["POST", "OPTIONS"])
def toggle_room(room_id):
    return light_provider.toggle_room(room_id)


# Toggle specific unit in specific room
@app.route("/toggle/room/<int:room_id>/unit/<string:unit_id>", methods=["POST", "OPTIONS"])
def toggle_room_unit(room_id, unit_id):
    return light_provider.toggle_unit(room_id, unit_id)


# Send remote signal for specific remote with lirc specified key
@app.route("/remote/<int:remote_id>/key/<string:key>", methods=["POST", "OPTIONS"])
def remote(remote_id, key):
    return ir_provider.send_command(remote_id, key)


# Send multiple remote signals according to a percentage value
@app.route("/remote/<int:remote_id>/volume/<mode>/<float:percentage>", methods=["POST", "OPTIONS"])
def set_volume(remote_id, mode, percentage):
    if mode == "up":
        return ir_provider.set_volume(remote_id, percentage)
    elif mode == "down":
        return ir_provider.set_volume(remote_id, -percentage)
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
