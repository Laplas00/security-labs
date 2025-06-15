import os

def get_vuln_flag():
#    raw = os.getenv("vulnerability", "")
    flag = 'sql_inj_classic'
    return flag 
    #'2fa_bypass_weak_logic'
    #'auth_bypass_forgotten_cookie'
    #'idor_bac,reflected_xss'

    #return [flag.strip().lower() for flag in raw.split(",") if flag.strip()]




