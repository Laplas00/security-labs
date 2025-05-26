from flask import Flask, request, jsonify
import subprocess
import os
import json
import random
import jwt



app = Flask(__name__)
BASE_PORT = 8100
MAX_PORT = 8199
NGINX_SITES = "/etc/nginx/sites-enabled/"

def get_free_port():
    for port in range(BASE_PORT, MAX_PORT):
        result = subprocess.run(['lsof', '-i', f':{port}'], stdout=subprocess.PIPE)
        if not result.stdout:
            return port
    raise Exception("No free ports available")

@app.route("/start_lab", methods=["POST"])
def start_lab():
    data = request.get_json()
    token = data.get("token")

    try:
        payload = jwt.decode(token, "SomeSecret22", algorithms=["HS256"])
        user = data.get("user", False)

        if user == False:
            return jsonify({'error':'User False'})

        lab = data.get("lab", None)
        if lab is None:
            return jsonify({'error':'lab None'})

        subdomain = f"for-{user}-{lab}"
        port = get_free_port()

        # Запускаем контейнер
        subprocess.run([
            "docker", "run", "-d",
            "--name", subdomain,
            "-p", f"{port}:80",
            "--memory", "150m", "--cpus", "0.05",
            f"lab_{lab}"
        ])

        # Генерируем nginx конфиг
        nginx_conf = f"""
server {{
    listen 80;
    server_name {subdomain}.labs-is-here.online;

    location / {{
        proxy_pass http://127.0.0.1:{port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }}
}}
    """
        conf_path = f"/etc/nginx/sites-enabled/{subdomain}"
        with open(conf_path, "w") as f:
            f.write(nginx_conf)

        subprocess.run(["nginx", "-t"])
        subprocess.run(["systemctl", "reload", "nginx"])

        return jsonify({
            "status": "ok",
            "url": f"http://{subdomain}.labs-is-here.online"
        })


    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 403
    except Exception:
        return jsonify({"error": "Invalid token"}), 403
        user = data.get("user", False)
        if user == False:
            return jsonify({'error':'User False'})
        lab = data.get("lab", "xss")
        subdomain = f"lab-{user}"
        port = get_free_port()

        # Запускаем контейнер
        subprocess.run([
            "docker", "run", "-d",
            "--name", subdomain,
            "-p", f"{port}:80",
            "--memory", "150m", "--cpus", "0.05",
            f"lab_{lab}"
        ])

        # Генерируем nginx конфиг
        nginx_conf = f"""
    server {{
        listen 80;
        server_name {subdomain}.labs-is-here.online;

        location / {{
            proxy_pass http://127.0.0.1:{port};
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }}
    }}
    """
        conf_path = f"/etc/nginx/sites-enabled/{subdomain}"
        with open(conf_path, "w") as f:
            f.write(nginx_conf)

        subprocess.run(["nginx", "-t"])
        subprocess.run(["systemctl", "reload", "nginx"])

        return jsonify({
            "status": "ok",
            "url": f"http://{subdomain}.labs-is-here.online"
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

