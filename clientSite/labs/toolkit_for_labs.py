from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_list_or_404
from django.urls import reverse

from datetime import datetime, timedelta
import requests, jwt
from icecream import ic


SECRET_KEY = "SomeSecret22"
ALGORITHM = "HS256"
EDGE_IP = "http://207.231.109.77:5000"

def get_lab_status(user, lab, token):
    data = {
        "user": user,
        "lab": lab,
        "token": token
    }
    r = requests.post(f"{EDGE_IP}/get_lab_status_for_user", json=data, timeout=5)
    print('----')
    ic(r.json())
    return r.json()

def get_runned_container(user):
    data = {"user": user,}
    r = requests.post(f"{EDGE_IP}/get_runned_container", json=data, timeout=5)
    data = r.json()
    if data['message'] == []:
        return ''
    if data['message'][0].startswith('Error'):
        return ''
    return data['message'][0].split('-')[1]


def generate_lab_token(user: str, lab: str):
    payload = {
        "user": user,
        "lab": lab,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token

@login_required
def toggle_lab_vuln(request):
    user = f"{request.user.username}{request.user.id}"
    lab = request.POST.get("lab")

    data = {
        "user": user,
        "lab": lab,
        "vulnerability":lab,
        "jwttoken": generate_lab_token(user, lab),
    }

    try:
        r = requests.post(f"{EDGE_IP}/toggle_vuln", json=data)
        return JsonResponse(r.json())
    except Exception as e:
        return JsonResponse({"error": str(e)})

@login_required 
def start_lab(request): 
    ic('start lab')
    ic(request)
    user = f"{request.user.username}{request.user.id}"
    lab = request.POST.get("lab")
    ic(lab)
    data = {
        "user": user,
        "lab": lab,
        'vulnerability':lab,
        "jwttoken": generate_lab_token(user, lab),
    }

    try:
        r = requests.post(f"{EDGE_IP}/start_lab", json=data)
        print('start lab request.post')
        print(r)
        return redirect('lab_view', container_name=lab)

    except Exception as e:
        print('erorr while starting lab')
        print(e)
        return JsonResponse({"error": str(e)})

@login_required
def stop_lab(request):
    user = f"{request.user.username}{request.user.id}"
    ic(user)
    lab = request.POST.get("lab")
    ic(lab)

    data = {
        "user": user,
        "lab": lab,
        "jwttoken": generate_lab_token(user, lab),
    }
    ic(data)

    try:
        r = requests.post(f"{EDGE_IP}/stop_lab", json=data)
        return redirect('lab_view', container_name=lab)

    except Exception as e:
        ic(e)
        return JsonResponse({"error": str(e)})

