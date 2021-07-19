from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return {"temperature": {"Celsius": 23, "Farent": 42}}
