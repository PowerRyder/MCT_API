
from src.utilities.utils import execute_query


def get_admin_details(admin_user_id:str):
    res = execute_query("call usp_get_admin_details(_admin_user_id => %s)", (admin_user_id,))
    return res

    
def get_admin_dashboard_details(admin_user_id:str):
    res = execute_query("call usp_get_admin_dashboard_details(_admin_user_id => %s)", (admin_user_id,))
    return res


def get_admin_dashboard_chart_details(duration: str):
    res = execute_query("call usp_get_admin_dashboard_chart_details(_duration => %s)", (duration, ))
    return res
