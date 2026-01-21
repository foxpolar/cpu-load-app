from flask import Flask, render_template, request, redirect
import requests
import cpu_stress
import psutil

app = Flask(__name__)

METADATA_BASE = "http://169.254.169.254/latest"

def get_token():
    return requests.put(
        f"{METADATA_BASE}/api/token",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
        timeout=2
    ).text

def get_metadata(path, token):
    return requests.get(
        f"{METADATA_BASE}/meta-data/{path}",
        headers={"X-aws-ec2-metadata-token": token},
        timeout=2
    ).text

def get_instance_metadata():
    try:        
        token = get_token()
        instance_id = get_metadata("instance-id", token)
        az = get_metadata("placement/availability-zone", token)
        return instance_id, az
    except:
        return "local-dev", "unknown"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "start":
            cpu_stress.start_cpu_load()
        elif action == "stop":
            cpu_stress.stop_cpu_load()
        return redirect("/")

    instance_id, az = get_instance_metadata()
    cpu_load = psutil.cpu_percent(interval=1)
    return render_template("index.html", instance_id=instance_id, az=az, cpu_load=cpu_load)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)