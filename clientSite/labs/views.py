from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def modules(request):
    return render(request, 'cards.html')

@login_required
def sql_classic(request):
    return render(request, 'labs/sql_injection_classic.html', 
                  context={'lab_name':'sql_classic'})

