
from src.utilities.utils import execute_query


def get_franchise_details(user_id:str):
    res = execute_query("call usp_get_franchise_details(_franchise_user_id => %s)", (user_id,))
    return res

    
def get_franchise_dashboard_details(user_id:str):
    res = execute_query("call usp_get_franchise_dashboard_details(_franchise_user_id => %s)", (user_id,))
    return res