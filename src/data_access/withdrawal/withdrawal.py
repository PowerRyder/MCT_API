from src.schemas.Withdrawal import GetWithdrawalRequests, WithdrawFund
from src.utilities.utils import execute_query


def withdraw_fund(req: WithdrawFund, user_id:str, user_type: str):
    res = execute_query("call usp_withdraw_fund(_user_id => %s, _user_type => %s,_wallet_id => %s, "
                        "_amount => %s, _remarks => %s, _two_factor_auth_request_id => %s,"
                        "_crypto_network => %s, _token_symbol => %s, _token_type => %s, _crypto_wallet_address => %s)",
    (user_id, user_type, req.wallet_id, req.amount, req.remarks, req.two_factor_auth_request_id,
     req.crypto_network, req.token_symbol, req.token_type, req.crypto_wallet_address))
    return res


def get_withdrawal_requests(req: GetWithdrawalRequests, match_exact_user_id: bool):
    res = execute_query("call usp_get_withdrawal_requests(_user_id => %s, _user_type => %s, _match_exact_user_id => %s, _request_date => %s::timestamptz[], _status => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, req.user_type, match_exact_user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.status, req.page_index, req.page_size))
    return res


def update_withdrawal_requests_status(by_user_id: str, data_dicts: list, enable_lock_only: bool = False):
    res = execute_query("call usp_update_withdrawal_request_status(_by_user_id => %s, _data => %s::jsonb, _enable_lock_only => %s)", 
                        (by_user_id, data_dicts, enable_lock_only))
    return res


def update_withdrawal_requests_status_crypto(request_id: int, status: str, remarks: str, txn_hash: str):
    res = execute_query("call usp_update_withdrawal_request_status_crypto(_request_id => %s, _status => %s, _remarks => %s, _txn_hash => %s)",
                        (request_id, status, remarks, txn_hash))
    return res


def unlock_withdrawal(data_dicts: list):
    res = execute_query("call usp_unlock_withdrawal_request(_data => %s)", (data_dicts, ))
    return res


def withdraw_principle(user_id:str, pin_srno: int, address: str, remarks: str = '', two_factor_auth_request_id: int = 0):
    res = execute_query("call usp_withdraw_principle(_user_id => %s, _pin_srno => %s, _address => %s, "
                        "_remarks => %s, _two_factor_auth_request_id => %s)",
    (user_id, pin_srno, address, remarks, two_factor_auth_request_id))
    return res


def update_withdrawal_requests_status_principle(pin_srno: int, status: str, txn_hash: str):
    res = execute_query("call usp_update_withdrawal_request_status_principle(_pin_srno => %s, _status => %s, _txn_hash => %s)",
                        (pin_srno, status, txn_hash))
    return res
