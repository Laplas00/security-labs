from flask import Flask, request, jsonify
import subprocess
import random
import string
import os

app = Flask(__name__)

TRAEFIK_NETWORK = "bridge"  # если используешь docker network traefik, пропиши тут имя

# Демо-валидация токена
def verify_jwt(token):
    # Здесь будет реальная проверка JWT — сейчас просто заглушка
    return token == "SomeSecret22"

def get_free_port(start=8100, end=8199):
    # Находим свободный порт (очень примитивно, для MVP)
    used_ports = subprocess.getoutput("docker ps --format '{{.Ports}}'").split('\n')
    for port in range(start, end):
        if not any(f':{port}->' in x for x in used_ports):
            return port
    raise Exception("Нет свободных портов!")

@app.route("/start_lab", methods=["POST"])
def start_lab():
    data = request.get_json()
    user = data.get("user")
    lab = data.get("lab")
    token = data.get("jwttoken")

    if not all([user, lab, token]):
        return jsonify({"error": "user, lab, and jwttoken are required"}), 400

    if not verify_jwt(token):
        return jsonify({"error": "Invalid JWT token"}), 403

    # Генерируем уникальное имя контейнера: <user>-<lab>
    container_name = f"{user}-{lab}"

    # Проверяем, не запущен ли уже такой контейнер
    existing = subprocess.getoutput(f"docker ps -a --format '{{{{.Names}}}}' | grep ^{container_name}$")
    if existing:
        return jsonify({"error": "Lab already running for this user!"}), 409

    # Находим свободный порт
    port = get_free_port()

    # Пример простейшего Flask-сайта как лаба (замени на свой образ)
    image = "pallets/flask"  # можно собрать свой lab_xss и т.д.

    # Запускаем контейнер с traefik labels
    run_command = [
        "docker", "run", "-d",
        "--name", container_name,
        "-l", f"traefik.enable=true",
        "-l", f"traefik.http.routers.{container_name}.rule=Host(`{container_name}.labs-is-here.online`)",
        "-l", f"traefik.http.routers.{container_name}.entrypoints=web",
        "-l", f"traefik.http.services.{container_name}.loadbalancer.server.port=5000",
        "-p", f"{port}:5000",
        image,
        "flask", "run", "--host=0.0.0.0"
    ]

    try:
        subprocess.run(run_command, check=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "status": "ok",
        "url": f"http://{container_name}.labs-is-here.online",
        "port": port,
        "container": container_name
    })

@app.route("/stop_lab", methods=["POST"])
def stop_lab():
    data = request.get_json()
    user = data.get("user")
    lab = data.get("lab")
    token = data.get("jwttoken")

    if not all([user, lab, token]):
        return jsonify({"error": "user, lab, and jwttoken are required"}), 400

    if not verify_jwt(token):
        return jsonify({"error": "Invalid JWT token"}), 403

    container_name = f"{user}-{lab}"

    # Проверяем, существует ли контейнер
    existing = subprocess.getoutput(f"docker ps -a --format '{{{{.Names}}}}' | grep ^{container_name}$")
    if not existing:
        return jsonify({"error": "Lab is not running!"}), 404

    # Останавливаем и удаляем контейнер
    subprocess.run(["docker", "rm", "-f", container_name])

    return jsonify({"status": "stopped", "container": container_name})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

