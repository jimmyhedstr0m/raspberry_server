from flask import Flask, request
import json

app = Flask(__name__)

def init():
    with open("config.json") as json_data:
        d = json.load(json_data)
        print json.dumps(d)

@app.route("/")
def hello():
    return "Hello world!"

@app.route("/status")
def status():
    return "Working fine..."

@app.route("/lamps/toggle/<int:group>/<int:lamp>", methods=["POST"])
def toggle(group, lamp):
    return "Toggle group " + str(group) + " and lamp " + str(lamp)

@app.route("/remote", methods=["POST"])
def remote():
    return json.dumps(request.json)

if __name__ == "__main__":
    init()
    app.run()
