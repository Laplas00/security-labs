from flask import Flask, request
import os

# основной Flask (app)
app = Flask(__name__)

# внутренний сервер (api_app)
api_app = Flask('internal_api')

@api_app.route('/cgi-bin/vuln')
def vuln():
    ua = request.headers.get('User-Agent', '')
    print(f"[INTERNAL_API] Получен User-Agent: {ua}")
    if 'shellshock' in ua:
        return "FLAG{ssrf_shellshock_worked}"
    return "Hello from CGI!"

def run_internal_api():
    # static_folder=None
    api_app.run(host='127.0.0.1', port=8080, use_reloader=True, debug=False)

