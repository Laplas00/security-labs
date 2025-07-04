import os

def get_vuln_flag():
    flag = os.getenv("vulnerability", "")
    flag = 'stored_xss'
    return flag 

