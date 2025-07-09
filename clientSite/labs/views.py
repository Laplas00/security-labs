from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .toolkit_for_labs import generate_lab_token,  get_lab_status, get_runned_container
from icecream import ic
from .models import LabModule
from django.shortcuts import render, get_object_or_404



@login_required
def dashboard(request): 
    user = f"{request.user.username.lower()}{request.user.id}"
    runned = get_runned_container(user)
    ic(runned)
    cards = LabModule.objects.all().order_by('tier', 'lab_name')
    ic(cards)
    return render(request, 'dashboard.html', {'runned':runned})

@login_required
def modules(request):
    user = f"{request.user.username.lower()}{request.user.id}"
    runned = get_runned_container(user)
    ic(runned)

    cards = LabModule.objects.all()
    categories = []
    fast_flash = [categories.append(x.category) for x in cards if x.category not in categories]
    ic(cards)
    ic(fast_flash)
    return render(request, 'cards.html', context={'cards': cards,
                                                  'runned':runned})

@login_required
def lab_view(request, container_name):
    print('lab view is runned')
    user = f"{request.user.username.lower()}{request.user.id}"
    token = generate_lab_token(user, container_name)
    status = get_lab_status(user, container_name, token)

    lab = get_object_or_404(LabModule, container_name=container_name)
    ic(lab)
    return render(request, 'labs/lab_detail.html', {
        'lab':lab,
        'status': status,
        'runned': '',
        # 'vuln_mode': status.get('mode', ''), 
    })


