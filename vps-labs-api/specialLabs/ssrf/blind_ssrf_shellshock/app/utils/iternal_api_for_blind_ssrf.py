
from flask import Flask, request

api_app = Flask('internal_api')


@api_app.route('/cgi-bin/vuln')
def vuln():
    ua = request.headers.get('User-Agent', '')
    print(f"[INTERNAL_API] Получен User-Agent: {ua}", flush=True)
    # BLIND: запускаем curl на внешний адрес (webhook.site)
    import os
    import re

    # Попробуем выцепить адрес из UA — можно прямо заменить YOUR-SERVER на свой, если лабы закрытые
    # Или просто всегда curl на твой webhook (демка)
    m = re.search(r'(https?://[^\s]+)', ua)
    if m:
        target = m.group(1)
        os.system(f"curl {target}")
    else:
        # Если вдруг не нашли URL — хотя бы вызовем твой webhook статически
        print('No url. Else statement.')
    # Возвращать флаг не надо — пусть будет blind!
    return "Hello from CGI!"

def run_internal_api():
    api_app.run(host='127.0.0.1', port=8080, debug=False, use_reloader=False)

