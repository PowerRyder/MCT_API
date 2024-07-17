
from src.schemas.Pin import PinTransferHistoryRequest, PinTransferRequest
from src.utilities.utils import execute_query


def get_available_pin_count_for_transfer(userId: str, packageId: int):
    res = execute_query("call usp_get_available_pin_count_for_transfer(_user_id => %s, _package_id => %s)", (userId, packageId))
    return res

def transfer_pins(req: PinTransferRequest, by_user_id: str):
    res = execute_query("call usp_transfer_pins(_from_user_id => %s, _by_user_id => %s, _to_user_id => %s, _package_id => %s, _no_of_pins_to_transfer => %s, _remarks => %s, _two_factor_auth_request_id => %s)", 
                        (req.from_user_id, by_user_id, req.to_user_id, req.package_id, req.no_of_pins, req.remarks, req.two_factor_auth_request_id))
    return res

def get_pin_transfer_history(req: PinTransferHistoryRequest, match_exact_from_user_id: bool, match_exact_to_user_id: bool):
    res = execute_query("call usp_get_pin_transfer_history(_from_user_id => %s, _from_user_type => %s, _match_exact_from_user_id => %s, _match_exact_to_user_id => %s, _to_user_id => %s, _to_user_type => %s, _package_id => %s, _between_date => %s::timestamptz[], _page_index => %s, _page_size => %s)",
                        (req.from_user_id, req.from_user_type, match_exact_from_user_id, match_exact_to_user_id, req.to_user_id, req.to_user_type, req.package_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.page_index, req.page_size))
    return res
