from flask import Flask, render_template, request, redirect
import requests
import cpu_stress
import psutil

app = Flask(__name__)

def get_instance_metadata():
    try:
        instance_id = requests.get("http://169.254.169.254/latest/meta-data/instance-id", timeout=2).text
        az = requests.get("http://169.254.169.254/latest/meta-data/placement/availability-zone", timeout=2).text
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