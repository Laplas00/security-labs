import os

def get_vuln_flags():
    raw = os.getenv("vulnerabilities", "")
    return [flag.strip().lower() for flag in raw.split(",") if flag.strip()]
