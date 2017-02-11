from flask import Flask, request, abort
import json

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello world!"


@app.route("/status")
def status():
    return "Working fine..."


@app.route("/switches/toggle/<int:group>/<unit>", methods=["POST"])
def toggle(group, unit):
    if unit == "all":
        return "Toggle all units in group " + str(group)
    else:
        try:
            unit = int(unit)
            return "Toggle group " + str(group) + " and unit " + str(unit)
        except ValueError:
            abort(400)


@app.route("/remote", methods=["POST"])
def remote():
    return json.dumps(request.json)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
