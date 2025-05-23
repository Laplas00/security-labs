from flask import Flask, request, jsonify
from lab_manager import start_lab, stop_lab

app = Flask(__name__)

@app.route("/start_lab", methods=["POST"])
def start():
    data = request.get_json()
    lab_type = data.get("lab", "xss")  # временно фиксированная лаба
    port = start_lab(lab_type)  # возвращает порт + ссылку
    return jsonify({"status": "ok", "port": port, "url": f"http://your-vps-ip:{port}"})

@app.route("/stop_lab", methods=["POST"])
def stop():
    data = request.get_json()
    port = data.get("port")
    stop_lab(port)
    return jsonify({"status": "stopped", "port": port})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

