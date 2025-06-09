
from flask import Flask, request, make_response, redirect
from datetime import datetime

app = Flask(__name__)

# 💥 Это условие симулирует кэш: если URL = "/cached", он может быть "отравлен"
@app.route('/cached', methods=['GET', 'POST'])
def cached():
    # Просто показываем, какой сейчас был "пользователь" — это будет перезаписано "отравлением"
    username = request.args.get('user', 'guest')

    # Возвращаем кэшируемый ответ
    resp = make_response(f"<h1>Welcome {username}</h1>")
    resp.headers['X-Cacheable'] = 'YES'  # Намёк, что может быть закэшировано
    return resp

# 💬 Заглушка на "пост-запрос" — мы её будем использовать как вредную часть smuggling
@app.route('/submit', methods=['POST'])
def submit():
    # Просто подтверждаем, что POST был принят
    return "Post request received", 200

# 🔍 Главная страница с информацией
@app.route('/')
def index():
    return '''
    <h1>Welcome to vulnerable smuggling lab</h1>
    <ul>
      <li><a href="/cached?user=guest">Visit cached page</a></li>
    </ul>
    <form method="POST" action="/submit">
      <input type="text" name="msg" placeholder="send POST" />
      <button type="submit">Send</button>
    </form>
    '''

# 🔒 Для запуска
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

