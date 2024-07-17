

from src.schemas.Pin import PinStatisticsRequest, ViewPinRequest
from src.utilities.utils import execute_query


def get_pin_details(pinNumber: str, pinPassword: str):
    res = execute_query("call usp_check_pin_validity(_pin_number => %s, _pin_password => %s)", (pinNumber, pinPassword))
    return res

def view_pins(req: ViewPinRequest, match_exact_user_id):
    res = execute_query("call usp_view_pins(_user_id => %s, _user_type => %s, _package_id => %s, _match_exact_user_id => %s, _between_date => %s::timestamptz[], _used_status => %s, _pin_generate_request_id => %s, _pin_transfer_request_id => %s, _pin_request_id => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, req.user_type, req.package_id, match_exact_user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.used_status, req.pin_generate_request_id, req.pin_transfer_request_id, req.pin_request_id, req.page_index, req.page_size))
    return res

def pin_statistics(req: PinStatisticsRequest, match_exact_user_id: bool):
    res = execute_query("call usp_get_pin_statistics(_user_id => %s, _user_type => %s, _match_exact_user_id => %s, _package_id => %s, _date => %s::timestamptz[], _page_index => %s, _page_size => %s)",
                        (req.user_id, req.user_type, match_exact_user_id, req.package_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.page_index, req.page_size))
    return res