import os

def get_vuln_flag():
    flag = os.getenv("vulnerability", "")
    flag = '2fa_bypass_weak_logic'
    return flag 

