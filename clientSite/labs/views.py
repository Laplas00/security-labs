from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .toolkit_for_labs import generate_lab_token,  get_lab_status
from icecream import ic
# from .models import LabModule
from django.shortcuts import render, get_object_or_404



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
                {'name':'idor_bac', #idor brocen access control  
                 'tier': 'easy',
                 'description':'URL/parameter tampering, missing ownership check',
                },
                {'name':'2fa_bypass_weak_logic',
                 'tier': 'easy',
                 'description':'Most complex - mulsti step, proxy manipulation',
                },
                {'name':'auth_bypass_forgotten_cookie',
                 'tier': 'easy',
                 'description':'nope',
                },
                {'name':'reflected_xss',
                 'tier': 'easy',
                 'description':'nope',
                },
                {'name':'clobbering_dom_attr_to_bp_html_filters',
                 'tier': 'medium',
                 'description':'nope',
                },
                {'name':'ssti_via_jinja2',
                 'tier': 'hard',
                 'description':'nope',
                },
                {'name':'blind_ssrf_shellshock',
                 'tier': 'hard',
                 'description':'single-step, JSON/response manipulation',
                },
                {'name':'xxe_repurpose_local_dtd',
                 'tier': 'hard',
                 'description':'',
                },
                {'name':'http_request_smuggling_cache_poison',
                 'tier': 'hard',
                 'description':'000',
                },
                {'name':'ssrf_whitelist_based_bypass',
                 'tier': 'hard',
                 'description':'000',
                },
                {'name':'xss_angular_sandbox_escape',
                 'tier': 'hard',
                 'description':'000',
                },
                {'name':'command_injection_basic',
                 'tier': 'easy',
                 'description':'000',
                },
                {'name':'xxe_via_xml_post',
                 'tier': 'easy',
                 'description':'000',
                },
             ]
    print("==== DEBUG cards ====")
    for c in cards:
        print(c)
    # cards = LabModule.objects.all().order_by('tier', 'lab_name')
    return render(request, 'cards.html', context={'cards': cards})


@login_required
def lab_view(request, lab_name):
    user = f"{request.user.username.lower()}{request.user.id}"
    token = generate_lab_token(user, lab_name)
    status = get_lab_status(user, lab_name, token)

    return render(request, f'labs/{lab_name}.html', {
        'lab_name': lab_name,
        'status': status
    })
# @login_required
# def lab_view(request, lab_name):
#     user = f"{request.user.username.lower()}{request.user.id}"
#     token = generate_lab_token(user, lab_name)
#     status = get_lab_status(user, lab_name, token)
#
#     card = get_object_or_404(LabModule, container_name=lab_name)
#
#     return render(request, 'lab_detail.html', {
#         'card': card,
#         'status': status,
#         'vuln_mode': status.get('mode', ''),  # если у тебя есть это поле
#         # можно добавить другие динамические параметры
#     })
#

@login_required
def template_site(request):
    user = request.user.username.lower()
