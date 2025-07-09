from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .toolkit_for_labs import generate_lab_token,  get_lab_status, get_runned_container
from icecream import ic
from .models import LabModule
from django.shortcuts import render, get_object_or_404, get_list_or_404
from itertools import groupby
from operator import attrgetter


def get_category_with_labs():
    cards = LabModule.objects.order_by('category', 'container_name')
    return {category: list(group)
            for category, group in groupby(cards, key=attrgetter('category'))}

@login_required
def dashboard(request): 
    user = f"{request.user.username.lower()}{request.user.id}"
    runned = get_runned_container(user)
    ic(runned) 
    return render(request, 'dashboard.html', {'runned':runned, 'categories': get_category_with_labs()})

@login_required
def modules(request):
    user = f"{request.user.username.lower()}{request.user.id}"
    runned = get_runned_container(user)
    ic(runned)   
    return render(request, 'cards.html', context={'categories': get_category_with_labs(),
                                                  'runned':runned})

@login_required
def lab_view(request, container_name):
    print('lab view is runned')
    user = f"{request.user.username.lower()}{request.user.id}"
    token = generate_lab_token(user, container_name)
    status = get_lab_status(user, container_name, token)

    labs = get_list_or_404(LabModule, container_name=container_name)
    lab = labs[0]
    ic(lab)
    return render(request, 'labs/lab_detail.html', {
        'lab':lab,
        'status': status['status'],
        'runned': '',
        'categories': get_category_with_labs(),
        # 'vuln_mode': status.get('mode', ''), 
    })


