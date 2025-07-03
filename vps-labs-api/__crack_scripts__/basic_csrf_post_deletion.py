import requests
from icecream import ic

r = requests.get('http://lap3-basic_csrf.labs-is-here.online/delete_post/2')

ic(r.text)
