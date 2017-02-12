from flask import Flask, make_response, request, abort
from config_parser import ConfigParser
from ir_remote import IrRemote
import crossdomain_fix
import json

app = Flask(__name__)
config_parser = ConfigParser()
ir_remote = IrRemote(0)


@app.route("/")
def hello():
    return "Hello world!"


@app.route("/status")
def status():
    return "Working fine..."


@app.route("/switches/toggle/<int:group>/<unit>", methods=["POST"])
def toggle(group, unit):
    if unit == "all":
        print json.dumps(config_parser.get_switch_groups(), indent=2, sort_keys=True)
        return "Toggle all units in group " + str(group)
    else:
        try:
            unit = int(unit)
            return "Toggle group " + str(group) + " and unit " + str(unit)
        except ValueError:
            abort(400)


@app.route("/remote", methods=["POST", "OPTIONS"])
@crossdomain_fix.crossdomain(origin='*')
def remote():
    print json.dumps(request.json, indent=2, sort_keys=True)
    command = request.json["command_id"]
    ir_remote.execute_command(command) 
    return(command)

if __name__ == "__main__":
    server_port = config_parser.get_server_port()
    app.run(host="0.0.0.0", port=server_port, debug=True)

