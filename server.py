from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"

@app.route("/<name>")
def name(name):
    return "Hello " + str(name)

if __name__ == "__main__":
    app.run()
