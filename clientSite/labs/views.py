from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .toolkit_for_labs import generate_lab_token,  get_lab_status


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def modules(request):
    return render(request, 'cards.html')

@login_required
def sql_classic(request):
    lab_name = "sql_inj_classic"
    user = f"{request.user.username.lower()}{request.user.id}"
    token = generate_lab_token(user, lab_name)
    status = get_lab_status(user, lab_name, token)
    return render(request, f'labs/{lab_name}.html', 
                  context={'lab_name':lab_name,
                           'status':status})

@login_required
def sql_bypass_auth(request):
    lab_name = "sql_bp_auth"
    user = f"{request.user.username.lower()}{request.user.id}"
    token = generate_lab_token(user, lab_name)
    status = get_lab_status(user, lab_name, token)
    return render(request, 'labs/{lab_name}.html', 
                  context={'lab_name':lab_name,
                           'status':status})

@login_required
def template_site(request):
    user = request.user.username.lower()
