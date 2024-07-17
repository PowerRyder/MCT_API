

from src.schemas.Pin import PinGenerateRequest
from src.utilities.utils import execute_query


def generate_pins(req: PinGenerateRequest, by_user_id: str, by_user_type: str):
    res = execute_query("call usp_generate_pins(_to_user_id => %s, _to_user_type => %s, _by_user_id => %s, _by_user_type => %s, _package_id => %s, _pin_value => %s, _pin_value_paid => %s, _wallet_id => %s, _no_of_pins => %s, _generation_user_remarks => %s, _two_factor_auth_request_id => %s)", 
                        (req.to_user_id, req.to_user_type, by_user_id, by_user_type, req.package_id, req.pin_value, req.pin_value_paid, req.wallet_id, req.no_of_pins, req.generation_user_remarks, req.two_factor_auth_request_id))
    return res

def get_pin_generate_history(by_user_id: str, by_user_type: str, page_index: int, page_size: int):
    res = execute_query("call usp_get_pin_generate_history(_user_id => %s, _user_type => %s, _page_index => %s, _page_size => %s)", 
                        (by_user_id, by_user_type, page_index, page_size))
    return res