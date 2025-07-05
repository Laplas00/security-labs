import os

def get_vuln_flag():
    flag = os.getenv("vulnerability", "")
    return 'dom_based_cookie_manipulation'
    return flag 

