from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .toolkit_for_labs import generate_lab_token,  get_lab_status
from icecream import ic



@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def modules(request):
    cards = [
                {'name':'sql_inj_classic',
                 'tier': 'easy',
                 'description':'Understanding of classical SQl injection.',
                },
                {'name':'reflected_xss',
                 'tier': 'easy',
                 'description':'Understanding of reflected xss injection.',
                },
                {'name':'stored_xss',
                 'tier': 'easy',
                 'description':'example',
                },
                {'name':'idor_bac', #idor brocen access control  
                 'tier': 'easy',
                 'description':'URL/parameter tampering, missing ownership check',
                },
                {'name':'auth_bypass',
                 'tier': 'easy',
                 'description':'single-step, JSON/response manipulation',
                },
                {'name':'2fa_bypass',
                 'tier': 'easy',
                 'description':'Most complex - mulsti step, proxy manipulation',
                },
                {'name':'http_request_smuggling_web_cache_poisoning',
                 'tier': 'hard',
                 'description':'OMG this is should be hard',
                },
             ]
    print("==== DEBUG cards ====")
    for c in cards:
        print(c)

    return render(request, 'cards.html', context={'cards':cards})

@login_required
def lab_view(request, lab_name):
    user = f"{request.user.username.lower()}{request.user.id}"
    token = generate_lab_token(user, lab_name)
    status = get_lab_status(user, lab_name, token)

    return render(request, f'labs/{lab_name}.html', {
        'lab_name': lab_name,
        'status': status
    })



@login_required
def template_site(request):
    user = request.user.username.lower()
