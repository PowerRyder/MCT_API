from src.schemas.Topup import RoiBlockUnblockRequest, TopupByPinRequest, TopupDetailsRequest, TopupFromWalletRequest
from src.utilities.utils import execute_query


def topup_by_pin(req: TopupByPinRequest, by_user_id: str, by_user_type: str):
    res = execute_query("call usp_topup_by_pin(_user_id => %s, _pin_number => %s, _pin_password => %s, _remarks => %s, _by_user_id => %s, _by_user_type => %s, _two_factor_auth_request_id => %s)",
                        (req.userId, req.pinNumber, req.pinPassword, req.remarks, by_user_id, by_user_type, req.two_factor_auth_request_id))
    return res


def topup_from_wallet(req: TopupFromWalletRequest, by_user_id: str, by_user_type: str):
    res = execute_query("call usp_topup_from_wallet(_user_id => %s, _package_id => %s, _pin_value => %s, _pin_value_paid => %s, _wallet_id => %s, _remarks => %s, _by_user_id => %s, _by_user_type => %s, _two_factor_auth_request_id => %s)",
                        (req.user_id, req.package_id, req.pin_value, req.pin_value_paid, req.wallet_id, req.remarks, by_user_id, by_user_type, req.two_factor_auth_request_id))
    return res


def topup_details(req: TopupDetailsRequest, match_exact_user_id: bool = False, match_exact_by_user_id: bool = False):
    res = execute_query("call usp_get_topup_details(_user_id => %s, _match_exact_user_id => %s, _between_date => %s::timestamptz[], _side => %s, _level => %s, _package_id => %s, _topup_type => %s, _topup_for => %s, _by_user_id => %s, _by_user_type => %s, _match_exact_by_user_id => %s, _pin_number => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, match_exact_user_id, [req.topup_date_from if req.topup_date_from!='' else None, req.topup_date_to if req.topup_date_to!='' else None], req.side, req.level, req.package_id, req.topup_type, req.topup_for, req.by_user_id, req.by_user_type, match_exact_by_user_id, req.pin_number, req.page_index, req.page_size))
    return res


def toggle_roi_block_status(req: RoiBlockUnblockRequest, by_admin_user_id: str):
    res = execute_query("call usp_toggle_roi_blocked_status(_pin_srno => %s, _status => %s, _by_admin_user_id => %s, _remarks => %s)",
                        (req.pin_srno, req.status, by_admin_user_id, req.remarks))
    return res


def delete_topup(pin_srno: int, remarks: str, by_admin_user_id: str):
    res = execute_query("call usp_delete_topup(_pin_srno => %s, _remarks => %s, _by_admin_user_id => %s)",
                        (pin_srno, remarks, by_admin_user_id))
    return res
