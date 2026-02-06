import subprocess
import yaml
import json
import re
from datetime import datetime


# ----------------------------
# Ping device and measure latency
# ----------------------------
def check_host(ip):
    try:
        result = subprocess.run(
            ["ping", "-n", "1", ip],  # Windows ping
            capture_output=True,
            text=True,
            timeout=3
        )

        output = result.stdout

        if "Reply from" in output:
            match = re.search(r"time[=<]\s*(\d+)", output)

            if match:
                latency = match.group(1) + "ms"
            else:
                latency = "-"

            return "UP", latency
        else:
            return "DOWN", "-"

    except Exception:
        return "DOWN", "-"


# ----------------------------
# Load YAML devices
# ----------------------------
def load_devices():
    with open("devices.yaml", "r") as f:
        return yaml.safe_load(f)


# ----------------------------
# Monitor all devices
# ----------------------------
def monitor_devices():
    devices = load_devices()
    results = []

    now = datetime.now().strftime("%H:%M:%S")

    for device in devices:
        status, latency = check_host(device["ip"])

        results.append({
            "name": device["name"],
            "ip": device["ip"],
            "status": status,
            "latency": latency,
            "last_checked": now
        })

    with open("logs.json", "w") as f:
        json.dump(results, f, indent=4)

    return results
