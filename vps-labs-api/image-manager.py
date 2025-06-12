import os
import json
import random
from flask import Flask, request, jsonify
import subprocess
import jwt
from icecream import ic
from time import sleep
from icecream import ic


bASE_PORT = 8100
MAX_PORT = 8199
app = Flask(__name__)
SECRET_KEY = "SomeSecret22"
ALGORITHM = "HS256"
DOMAIN = "labs-is-here.online"



@app.route("/start_lab", methods=["POST"])
def start_lab():
    data = request.get_json()
    token = data.get("jwttoken") or data.get("token")
    user = data.get("user").lower()
    lab = data.get("lab")
    vulnerabilities = data.get("vulnerabilities", "")  # ← Сюда передаёшь строку флагов, например "sql_inj_classic,idor_bac"
    print(vulnerabilities)
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 403
    except Exception as e:
        return jsonify({"error": f"Invalid token: {e}"}), 403

    if not all([user, lab]):
        return jsonify({"error": "user and lab required"}), 400

    subdomain = f"{user}-{lab}"

    # Проверяем что нет других контейнеров
    existing = subprocess.getoutput(
        f"docker ps -a --format '{{{{.Names}}}}' | grep '^{user}-'"
    )
    if existing.strip():
        return jsonify({"error": "You can run only one lab at a time!"}), 409

    docker_run = [
        'docker', 'run', '-d', '--name', f'{subdomain}',
        '--network', 'traefik-net',
        '-l', 'traefik.enable=true',
        '-l', f'traefik.http.routers.{subdomain}.rule=Host(\"{subdomain}.{DOMAIN}\")',
        '-l', f'traefik.http.routers.{subdomain}.entrypoints=web',
        '-l', f'traefik.http.services.{subdomain}.loadbalancer.server.port=5000',
        '-e', f'vulnerabilities={vulnerabilities}',
        '--memory', '150m', '--cpus', '0.05',
        "cyberlab_main"
    ]

    output = subprocess.run(docker_run, capture_output=True, text=True)
    sleep(2)
    return jsonify({
        "status": "ok",
        "url": f"http://{subdomain}.{DOMAIN}",
        "output": output.stdout,
        "vulnerabilities":vulnerabilities,
    })

@app.route("/toggle_vuln", methods=["POST"])
def toggle_vuln():
    data = request.get_json()
    token = data.get("jwttoken") or data.get("token")
    user = data.get("user").lower()
    lab = data.get("lab")
    vulnerabilities = data.get("vulnerabilities", "")

    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 403
    except Exception as e:
        return jsonify({"error": f"Invalid token: {e}"}), 403

    if not all([user, lab]):
        return jsonify({"error": "user and lab required"}), 400

    subdomain = f"{user}-{lab}"

    # Удаляем старый контейнер
    subprocess.run(["docker", "rm", "-f", subdomain])

    # Запускаем новый с обновлёнными флагами
    docker_run = [
        'docker', 'run', '-d', '--name', f'{subdomain}',
        '--network', 'traefik-net',
        '-l', 'traefik.enable=true',
        '-l', f'traefik.http.routers.{subdomain}.rule=Host(\"{subdomain}.{DOMAIN}\")',
        '-l', f'traefik.http.routers.{subdomain}.entrypoints=web',
        '-l', f'traefik.http.services.{subdomain}.loadbalancer.server.port=5000',
        '-e', f'vulnerabilities={vulnerabilities}',
        '--memory', '150m', '--cpus', '0.05',
        "cyberlab_main"
    ]
    output = subprocess.run(docker_run, capture_output=True, text=True)
    sleep(2)
    return jsonify({
        "status": "ok",
        "vulnerabilities": vulnerabilities,
        "url": f"http://{subdomain}.{DOMAIN}",
        "docker_output": output.stdout,
    })


@app.route("/stop_lab", methods=["POST"])
def stop_lab():
    data = request.get_json()
    token = data.get("jwttoken") or data.get("token")
    user = data.get("user").lower()
    lab = data.get("lab")

    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        return jsonify({"error": f"Invalid token: {e}"}), 403

    if not user or not lab:
        return jsonify({"error": "user and lab required"}), 400

    subdomain = f"{user}-{lab}"
    # Проверим, существует ли контейнер
    check_cmd = f"docker ps -a --filter 'name=^{subdomain}$' --format '{{{{.Names}}}}'"
    existing = subprocess.getoutput(check_cmd)

    if existing.strip() == subdomain:
        subprocess.run(["docker", "rm", "-f", subdomain])
        return jsonify({
            "status": "stopped",
            "container": subdomain
        })
    else:
        return jsonify({
            "status": "not_found",
            "container": subdomain,
            "message": "No such lab container running for this user"
        }), 404

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

        # Проверяем, существует ли контейнер и он "up"
        ps_cmd = f"docker ps --filter 'name=^{subdomain}$' --filter 'status=running' --format '{{{{.Names}}}}'"
        existing = subprocess.getoutput(ps_cmd)

        if existing.strip() == subdomain:
            # Получаем список флагов из ENV контейнера
            inspect_cmd = [
                "docker", "inspect", "-f",
                "{{range .Config.Env}}{{println .}}{{end}}",
                subdomain
            ]
            envs = subprocess.check_output(inspect_cmd).decode().splitlines()
            vulnerabilities = ""
            for env in envs:
                if env.startswith("vulnerabilities="):
                    vulnerabilities = env.split("=", 1)[1].strip()
                    break

            return jsonify({
                "status": "running",
                "url": f"http://{subdomain}.{DOMAIN}",
                "vulnerabilities": vulnerabilities
            })
        else:
            return jsonify({
                "status": "not_running"
            })
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except Exception as e:
        return jsonify({'error': f'Exception: {e}'}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


