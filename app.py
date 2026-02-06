from flask import Flask, render_template
import json
from monitor import monitor_devices

app = Flask(__name__)


@app.route("/")
def dashboard():
    # refresh monitoring data each time page loads
    monitor_devices()

    with open("logs.json") as f:
        devices = json.load(f)

    return render_template("dashboard.html", devices=devices)


if __name__ == "__main__":
    app.run(debug=True)
