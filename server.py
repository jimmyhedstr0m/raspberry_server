from flask import Flask, make_response, request, abort, jsonify
from config_parser import ConfigParser
from ir_provider import IrProvider
from light_provider import LightProvider
from temperature import Temperature
from re import findall
from crossdomain_fix import crossdomain
import json
import subprocess


app = Flask(__name__)
config_parser = ConfigParser()
light_provider = LightProvider()
ir_provider = IrProvider()
temperature = Temperature()

# Change this to False on server
server_debug = False


# Get all rooms
@app.route("/rooms", methods=["GET"])
@crossdomain(origin='*')
def get_rooms():
    return jsonify(light_provider.get_all_rooms())


# Get specific room
@app.route("/room/<int:room_id>")
@crossdomain(origin='*')
def get_room(room_id):
    return jsonify(light_provider.get_room(room_id))


# Get specific unit in specific room
@app.route("/room/<int:room_id>/unit/<string:unit_id>")
@crossdomain(origin='*')
def get_room_unit(room_id, unit_id):
    return jsonify(light_provider.get_room_unit(room_id, unit_id))


# Toggle specific room
@app.route("/toggle/room/<int:room_id>", methods=["POST", "OPTIONS"])
@crossdomain(origin='*')
def toggle_room(room_id):
    return jsonify(light_provider.toggle_room(room_id))


# Toggle specific unit in specific room
@app.route("/toggle/room/<int:room_id>/unit/<string:unit_id>", methods=["POST", "OPTIONS"])
@crossdomain(origin='*')
def toggle_room_unit(room_id, unit_id):
    return jsonify(light_provider.toggle_unit(room_id, unit_id))


# Send remote signal for specific remote with lirc specified key
@app.route("/remote/<int:remote_id>/key/<string:key>", methods=["POST", "OPTIONS"])
@crossdomain(origin='*')
def remote(remote_id, key):
    return jsonify(ir_provider.send_command(remote_id, key))


# Send multiple remote signals according to a percentage value
@app.route("/remote/<int:remote_id>/volume/<mode>/<float:percentage>", methods=["POST", "OPTIONS"])
@crossdomain(origin='*')
def set_volume(remote_id, mode, percentage):
    if mode == "up":
        return jsonify(ir_provider.set_volume(remote_id, percentage))
    elif mode == "down":
        return jsonify(ir_provider.set_volume(remote_id, -percentage))
    else:
        abort(400)


@app.route("/temperature")
@crossdomain(origin='*')
def temp():
    return jsonify(temperature.get_temperature())


if __name__ == "__main__":
    server_port = config_parser.get_server_port()

    if not server_debug:
        subprocess.call("sudo service pilight start", shell=True)
        subprocess.call("sudo service pilight restart", shell=True) # fix?

    app.run(host="0.0.0.0", port=server_port, debug=server_debug)
