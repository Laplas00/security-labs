import os

def get_vuln_flag():
    flag = os.getenv("vulnerability", "")
    return flag 


