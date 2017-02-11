from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"

@app.route("/status")
def status():
    return "Working fine..."

@app.route("/lamps/toggle/<int:group>/<int:lamp>", methods=["POST"])
def toggle(group, lamp):
    return "Toggle group " + str(group) + " and lamp " + str(lamp)

if __name__ == "__main__":
    app.run()
