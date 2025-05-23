import subprocess
import json
import random
import os

CONTAINERS_FILE = "running_labs.json"
PORT_RANGE = range(8100, 8199)

def get_free_port():
    used_ports = set()
    if os.path.exists(CONTAINERS_FILE):
        with open(CONTAINERS_FILE) as f:
            data = json.load(f)
            used_ports = {int(x["port"]) for x in data.values()}
    for port in PORT_RANGE:
        if port not in used_ports:
            return port
    raise Exception("No free ports")

def start_lab(lab_type):
    port = get_free_port()
    container_name = f"{lab_type}_{random.randint(1000, 9999)}"
    subprocess.Popen([
        "docker", "run", "-d",
        "--name", container_name,
        "-p", f"{port}:80",
        "--memory", "150m", "--cpus", "0.05",
        f"lab_{lab_type}"
    ])
    _save_container(container_name, port, lab_type)
    return port

def stop_lab(port):
    if not os.path.exists(CONTAINERS_FILE):
        return
    with open(CONTAINERS_FILE, "r") as f:
        containers = json.load(f)
    for name, info in containers.items():
        if info["port"] == port:
            subprocess.run(["docker", "rm", "-f", name])
            del containers[name]
            break
    with open(CONTAINERS_FILE, "w") as f:
        json.dump(containers, f)

def _save_container(name, port, lab):
    if os.path.exists(CONTAINERS_FILE):
        with open(CONTAINERS_FILE, "r") as f:
            containers = json.load(f)
    else:
        containers = {}
    containers[name] = {"port": port, "lab": lab}
    with open(CONTAINERS_FILE, "w") as f:
        json.dump(containers, f)

