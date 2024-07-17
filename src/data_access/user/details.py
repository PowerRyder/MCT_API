
from src.utilities.utils import execute_query


def get_user_details(user_id:str):
    res = execute_query("call usp_get_user_details(_user_id => %s)", (user_id,))
    return res

    
def get_user_dashboard_details(user_id:str):
    res = execute_query("call usp_get_user_dashboard_details(_user_id => %s)", (user_id,))
    return res


def get_user_dashboard_chart_details(user_id:str, duration: str):
    res = execute_query("call usp_get_user_dashboard_chart_details(_user_id => %s, _duration => %s)", (user_id, duration))
    return res
