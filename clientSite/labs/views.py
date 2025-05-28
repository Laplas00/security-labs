from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from toolkit_for_labs import EDGE_IP


def get_lab_status(user, lab, token):
    data = {
        "user": user,
        "lab": lab,
        "token": token
    }
    r = requests.post(f"{EDGE_IP}/get_lab_status_for_user", json=data, timeout=5)
    return r.json()


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def modules(request):
    return render(request, 'cards.html')

@login_required
def sql_classic(request):
    return render(request, 'labs/sql_injection_classic.html', 
                  context={'lab_name':'sql_inj_classic'})

