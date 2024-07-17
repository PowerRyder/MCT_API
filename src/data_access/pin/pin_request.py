
from src.schemas.Pin import GetPinRequest
from src.utilities.utils import execute_query


def request_for_pins(user_id: str, user_type: str, payment_request_id: int, pins):
    res = execute_query("call usp_request_for_pins(_user_id => %s, _user_type => %s, _payment_request_id => %s, _pins => %s::json)", 
                        (user_id, user_type, payment_request_id, pins))
    return res


def get_pin_request(req: GetPinRequest, match_exact_user_id: bool):
    res = execute_query("call usp_get_pin_requests(_user_id => %s, _user_type => %s, _match_exact_user_id => %s, _request_date => %s::timestamptz[], _payment_mode => %s, _reference_number => %s, _status => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, req.user_type, match_exact_user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.payment_mode, req.reference_number, req.status, req.page_index, req.page_size))
    return res


def get_pin_request_details(req_id: int):
    res = execute_query("call usp_get_pin_request_details(_request_id => %s)", 
                        (req_id,))
    return res

def update_pin_requests_status(by_user_id: str, by_user_type: str, data_dicts: list):
    res = execute_query("call usp_update_pin_request_status(_by_user_id => %s, _by_user_type => %s, _data => %s::jsonb)", 
                        (by_user_id, by_user_type, data_dicts))
    return res