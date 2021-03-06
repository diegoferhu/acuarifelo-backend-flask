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
    import glob
    import time

    base_dir = "/sys/bus/w1/devices/"
    device_folder = glob.glob(base_dir + "28*")[0]
    device_file = device_folder + "/w1_slave"

    def read_temp_raw():
        f = open(device_file, "r")
        lines = f.readlines()
        f.close()
        return lines

    def read_temp():
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != "YES":
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2 :]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c, temp_f

    while True:
        temperature = read_temp()
        response = {"celsius": temperature[0], "fahrenheit": temperature[1]}
        time.sleep(1)
        emit("temperature", response)


if __name__ == "__main__":
    socketio.run(app)
