
    
from src.utilities.utils import execute_query


def insert_paid_payment_details(user_id:str, user_type: str, amount: float, payment_mode: str, reference_number: str, 
                                remarks: str, image_path: str):
    res = execute_query("call usp_insert_paid_payment_request_details(_user_id => %s, _user_type => %s, _amount => %s, _mode => %s, _reference_no => %s, _remarks => %s, _image_path => %s)", 
    (user_id, user_type, amount, payment_mode, reference_number, remarks, image_path))
    return res
