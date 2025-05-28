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
    user = request.user.username
    token = generate_lab_token(user, lab_name)
    status = get_lab_status(user, lab_name, token)
    return render(request, 'labs/sql_inj_classic.html', 
                  context={'lab_name':lab_name,
                           'status':status})

