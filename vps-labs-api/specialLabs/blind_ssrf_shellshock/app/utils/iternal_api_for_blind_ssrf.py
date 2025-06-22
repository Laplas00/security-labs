
from flask import Flask, request

api_app = Flask('internal_api')

@api_app.route('/cgi-bin/vuln')
def vuln():
    ua = request.headers.get('User-Agent', '')
    print(f"[INTERNAL_API] Получен User-Agent: {ua}", flush=True)
    if 'shellshock' in ua:
        return "FLAG{ssrf_shellshock_worked}"
    return "Hello from CGI!"

def run_internal_api():
    api_app.run(host='127.0.0.1', port=8080, debug=False, use_reloader=False)

