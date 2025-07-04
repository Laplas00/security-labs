import os

def get_vuln_flag():
    flag = os.getenv("vulnerability", "")
    flag = 'auth_bypass_forgotten_cookie'
    return flag 

