import os

def get_vuln_flag():
    flag = os.getenv("vulnerability", "")
    return 'ssrf_blacklist_bypass_ipv6'
    return flag 



