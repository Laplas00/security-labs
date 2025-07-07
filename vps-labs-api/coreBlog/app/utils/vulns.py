import os

def get_vuln_flag():
    flag = os.getenv("vulnerability", "")
    # return 'sql_union_column_number_discovery'
    # return 'blind_sql_injection_conditional'
    return 'blind_sql_injection_time_delay'
    return flag 

