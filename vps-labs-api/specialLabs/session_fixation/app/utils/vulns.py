import os

def get_vuln_flag():
    flag = os.getenv("vulnerability", "")
    # flag = 'session_fixation'
    return flag 



