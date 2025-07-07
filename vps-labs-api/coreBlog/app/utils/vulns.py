import os

def get_vuln_flag():
    flag = os.getenv("vulnerability", "")
    # return 'sql_union_column_number_discovery'
    return flag 

