
from flask import Flask, request, jsonify
import requests


api_app = Flask('internal_api')



@api_app.route('/check_comment')
def check_comment():
    url = request.args.get('url', '')
    print(f"[INTERNAL_API] Проверка ссылки: {url}", flush=True)
    try:
        # Проверяем ссылку — разрешаем редиректы (чтобы цепочка сработала!)
        resp = requests.get(url, timeout=3, allow_redirects=True)
        # Берём мета-инфу как в реальных сервисах проверки ссылок
        result = {
            'status': 'ok',
            'checked_url': resp.url,         # Куда реально дошли (после редиректов!)
            'http_code': resp.status_code,
            'content_type': resp.headers.get('Content-Type', ''),
            'preview': resp.text[:200],      # Первые 200 символов тела
        }
    except Exception as e:
        result = {
            'status': 'fail',
            'error': str(e)
        }
    return jsonify(result)

def run_internal_api():
    api_app.run(host='127.0.0.1', port=8080, debug=False, use_reloader=False)

