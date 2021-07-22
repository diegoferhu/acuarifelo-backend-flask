from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("get temperature")
def handle_get_temperature(json):
    print("received json: " + str(json))
    i = 1
    while i < 10:
        i = i + 1
        emit("my response", json)


if __name__ == "__main__":
    socketio.run(app)
