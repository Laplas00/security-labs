import requests
from icecream import ic

r = requests.get('http://0.0.0.0:8000/delete_post/2')

ic(r.text)
