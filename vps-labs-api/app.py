import os
import json
import random
from flask import Flask, request, jsonify
import subprocess
import jwt


bASE_PORT = 8100
MAX_PORT = 8199
app = Flask(__name__)
SECRET_KEY = "SomeSecret22"
ALGORITHM = "HS256"
DOMAIN = "labs-is-here.online"


@app.route("/get_lab_status_for_user", methods=["POST"])
def get_lab_status_for_user():
    data = request.get_json()
    token = data.get("token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = data.get("user", False)
        lab = data.get("lab", None)

        if not user:
            return jsonify({'error': 'User False'}), 400
        if not lab:
            return jsonify({'error': 'Lab None'}), 400

        subdomain = f"{user}-{lab}"
        # Проверяем, существует ли контейнер с таким именем и он "Up"
        ps_cmd = f"docker ps --filter 'name=^{subdomain}$' --filter 'status=running' --format '{{{{.Names}}}}'"
        existing = subprocess.getoutput(ps_cmd)

        if existing.strip() == subdomain:
            return jsonify({
                "status": "running",
                "url": f"http://{subdomain}.{DOMAIN}"
            })
        else:
            return jsonify({
                "status": "not_running"
            })
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except Exception as e:
        return jsonify({'error': f'Exception: {e}'}), 400


@app.route("/start_lab", methods=["POST"])
def start_lab():
    data = request.get_json()
    token = data.get("jwttoken") or data.get("token")
    user = data.get("user")
    lab = data.get("lab")

    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 403
    except Exception as e:
        return jsonify({"error": f"Invalid token: {e}"}), 403

    if not all([user, lab]):
        return jsonify({"error": "user and lab required"}), 400

    subdomain = f"{user}-{lab}"

    existing = subprocess.getoutput(f"docker ps -a --format '{{{{.Names}}}}' | grep ^{subdomain}$")
    if existing:
        return jsonify({"error": "Lab already running for this user!"}), 409

    docker_run = [
        "docker", "run", "-d",
        "--name", subdomain,
        "-l", f"traefik.enable=true",
        "-l", f"traefik.http.routers.{subdomain}.rule=Host(`{subdomain}.labs-is-here.online`)",
        "-l", f"traefik.http.routers.{subdomain}.entrypoints=web",
        "-l", f"traefik.http.services.{subdomain}.loadbalancer.server.port=5000",
        "--memory", "150m", "--cpus", "0.05",
        f"lab_{lab}"
    ]
    subprocess.run(docker_run)

    return jsonify({
        "status": "ok",
        "url": f"http://{subdomain}.labs-is-here.online"
    })


@app.route("/stop_lab", methods=["POST"])
def stop_lab():
    data = request.get_json()
    token = data.get("jwttoken") or data.get("token")
    user = data.get("user")
    lab = data.get("lab")

    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        return jsonify({"error": f"Invalid token: {e}"}), 403

    if not all([user, lab]):
        return jsonify({"error": "user and lab required"}), 400

    subdomain = f"for-{user}-{lab}"
    subprocess.run(["docker", "rm", "-f", subdomain])

    return jsonify({
        "status": "stopped",
        "container": subdomain
    })



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



