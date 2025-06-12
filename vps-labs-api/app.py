
# Новый подход: один image, разные флаги (vulnerabilities)

# Изменения:
# - Вместо lab_{lab} мы используем один docker image: cyberlab_main
# - Управляем уязвимостями через ENV-переменную "vulnerabilities=sql,xss,..."
# - В Flask-приложении внутри контейнера включаем логику через парсинг этой переменной
#
# Ниже — пример архитектуры в коде и краткий план действий

# Файл: app.py (или run.py)
from flask import Flask, request, jsonify
import subprocess
import jwt
import os

app = Flask(__name__)
SECRET_KEY = "somesecret22"
ALGORITHM = "HS256"
DOMAIN = "labs-is-here.online"

@app.route("/start_lab", methods=["POST"])
def start_lab():
    data = request.get_json()
    token = data.get("token")
    user = data.get("user").lower()
    vuln_flags = data.get("vulnerabilities", "")  # ex: "sql,xss,csrf"

    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        return jsonify({"error": str(e)}), 403

    subdomain = f"{user}"

    # Проверка уже запущенных контейнеров
    existing = subprocess.getoutput(
        f"docker ps -a --format '{{{{.Names}}}}' | grep '^{user}'"
    )
    if existing.strip():
        return jsonify({"error": "you can run only one lab at a time!"}), 409

    # Запуск одного основного контейнера с ENV-переменной
    docker_run = [
        'docker', 'run', '-d', '--name', subdomain,
        '--network', 'traefik-net',
        '-l', 'traefik.enable=true',
        '-l', f'traefik.http.routers.{subdomain}.rule=Host(\"{subdomain}.{DOMAIN}\")',
        '-l', f'traefik.http.routers.{subdomain}.entrypoints=web',
        '-l', f'traefik.http.services.{subdomain}.loadbalancer.server.port=5000',
        '-e', f'vulnerabilities={vuln_flags}',
        '--memory', '150m', '--cpus', '0.05',
        'cyberlab_main'
    ]

    output = subprocess.run(docker_run)
    return jsonify({
        "status": "ok",
        "url": f"http://{subdomain}.{DOMAIN}"
    })

# Внутри контейнера (cyberlab_main), приложение Flask парсит os.environ['vulnerabilities']
# и включает соответствующие уязвимости

# Пример внутри уязвимой логики:
# if 'sql' in os.getenv("vulnerabilities", "").split(','):
#     # сделать sql-инъекцию

# Таким образом мы не пересобираем образы, не плодим контейнеры, и развиваем одну codebase

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

