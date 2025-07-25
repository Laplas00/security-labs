import os
import json
import random
from flask import Flask, request, jsonify
import subprocess
import jwt
from icecream import ic
from time import sleep
from icecream import ic


app = Flask(__name__)
SECRET_KEY = "SomeSecret22"
ALGORITHM = "HS256"
DOMAIN = "labs-is-here.online"


SPECIAL_LABS = [
        'xss_angular_sandbox_escape',#+

        'blind_ssrf_shellshock',#+
        'ssrf_whitelist_based_bypass',#+
        'ssrf_blacklist_bypass_ipv6',
        'open_redirect_to_ssrf_chain',

        'xxe_repurpose_local_dtd',#+
        'blind_xxe_to_retrieve_data_via_error_messages',
        'xxe_via_xml_post', #+
        'xxe_to_perform_ssrf_attacks',

        'http_request_smuggling_cache_poison',#+
        'command_injection_basic', #+
        'session_fixation',
        'poc_confirming_cl_te',
        'poc_confirming_te_cl',
        'front_end_request_rewriting',

        'insecure_deserialization',
        'modifying_serialized_objects',
        'modifying_serialized_data_types',
        'using_app_func_to_exploit_insecure_deserialization',

        'blind_command_injection_time_delay',
        'blind_command_injection_oob_interaction',
        'command_injection_filter_bypass',
        ]
labs_to_open_9000port = ['poc_confirming_cl_te', 'poc_confirming_te_cl', 
                         'front_end_request_rewriting', 'xxe_to_perform_ssrf_attacks']

@app.route("/start_lab", methods=["POST"])
def start_lab():
    data = request.get_json()
    token = data.get("jwttoken") or data.get("token")
    user = data.get("user").lower()
    lab = data.get("lab")
    vulnerability = data.get("vulnerability", "")  
    print(vulnerability)
    print(data)
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
        return jsonify({"error": f"You can run only one lab at a time!, {existing}"}), 409

     # Определяем, какой образ запускать
    if lab in SPECIAL_LABS:
        image_name = lab  # Предполагаем, что образ называется как lab (можно вынести в мапу)
    else:
        image_name = "cyberlab_main"


    docker_run = [
        'docker', 'run', '-d', '--name', f'{subdomain}',
        '--network', 'traefik-net', 
        '-l', 'traefik.enable=true',
        '-l', f'traefik.http.routers.{subdomain}.rule=Host(\"{subdomain}.{DOMAIN}\")',
        '-l', f'traefik.http.routers.{subdomain}.entrypoints=web',
        '-l', f'traefik.http.services.{subdomain}.loadbalancer.server.port=8000',
        '-e', f'vulnerability={vulnerability}',
        '--memory', '150m', '--cpus', '0.05',
        f"{image_name}"
    ]

    if lab in labs_to_open_9000port:
        print('')
        docker_run.insert(5, '-p')
        docker_run.insert(6, '9000:9000')

    output = subprocess.run(docker_run, capture_output=True, text=True)
    print(f'Output: {output}')
    return jsonify({
        "status": "ok",
        "url": f"http://{subdomain}.{DOMAIN}",
        "output": output.stdout,
        "vulnerability":vulnerability,
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


@app.route("/get_runned_container", methods=['POST'])
def get_runned_container():
    data = request.get_json()

    try:
        user = data.get("user", False)

        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"],
            capture_output=True, text=True
        )
        names = result.stdout.strip().splitlines()
        ic(names)
        # Оставляем только те, которые с дефисом (user-lab)
        working_lab = [n for n in names if f"{user}-" in n] 
        
        return {'message': working_lab}
    
    except Exception as e:
        print("Erorr:", e)
        return {"message": f'Error: {e}'} 


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
            vulnerability = ""
            for env in envs:
                if env.startswith("vulnerability="):
                    vulnerability = env.split("=", 1)[1].strip()
                    break

            return jsonify({
                "status": "running",
                "url": f"http://{subdomain}.{DOMAIN}",
                "vulnerability": vulnerability
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


