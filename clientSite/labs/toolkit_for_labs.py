import requests
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import jwt



import jwt
from datetime import datetime, timedelta

SECRET_KEY = "SomeSecret22"  # общий секрет с edge
ALGORITHM = "HS256"

def generate_lab_token(user: str, lab: str):
    payload = {
        "user": user,
        "lab": lab,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

EDGE_API = "http://207.231.109.77:5000" 


@login_required 
def start_lab(request): 
    user = request.user.username
    lab = request.GET.get("lab", "xss")

    data = {
        "user": user,
        "lab": lab
    }

    try:
        r = requests.post(f"{EDGE_API}/start_lab", json=data)
        return JsonResponse(r.json())
    except Exception as e:
        return JsonResponse({"error": str(e)})

@login_required
def stop_lab(request):
    port = request.GET.get("port")
    if not port:
        return JsonResponse({"error": "port is required"})

    try:
        r = requests.post(f"{EDGE_API}/stop_lab", json={"port": int(port)})
        return JsonResponse(r.json())
    except Exception as e:
        return JsonResponse({"error": str(e)})

