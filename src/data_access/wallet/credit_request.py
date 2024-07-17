from src.schemas.Wallet import GetCreditRequests, RequestForCredit
from src.utilities.utils import execute_query


def request_for_credit(req: RequestForCredit, user_id:str, user_type: str, payment_request_id: int):
    res = execute_query("call usp_request_for_credit(_user_id => %s, _user_type => %s,_wallet_id => %s, _amount => %s, _payment_request_id => %s)", 
    (user_id, user_type, req.wallet_id, req.amount, payment_request_id))
    return res


def get_credit_request(req: GetCreditRequests, match_exact_user_id: bool):
    res = execute_query("call usp_get_credit_requests(_user_id => %s, _user_type => %s, _match_exact_user_id => %s, _request_date => %s::timestamptz[], _payment_mode => %s, _reference_number => %s, _status => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, req.user_type, match_exact_user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.payment_mode, req.reference_number, req.status, req.page_index, req.page_size))
    return res


def update_credit_requests_status(by_user_id: str, by_user_type: str, data_dicts):
    res = execute_query("call usp_update_credit_request_status(_by_user_id => %s, _by_user_type => %s, _data => %s::jsonb)", 
                        (by_user_id, by_user_type, data_dicts))
    return res
