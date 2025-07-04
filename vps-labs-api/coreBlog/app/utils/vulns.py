import os

def get_vuln_flag():
    flag = os.getenv("vulnerability", "")
    flag = 'reflected_xss'
    return flag 

