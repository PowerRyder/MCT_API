
from src.schemas.Income import GetAllIncome_Request, GetTotalIncome_Request, PayPayoutAmount_Request
from src.utilities.utils import execute_query


def get_all_income(req: GetAllIncome_Request, match_exact_user_id: bool = False):
    res = execute_query("call usp_get_all_income(_user_id => %s, _match_exact_user_id => %s, _type => %s, _between_date => %s::timestamptz[], _total_income_payout_no => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, match_exact_user_id, req.type, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.total_income_payout_no, req.page_index, req.page_size))
    return res


def get_total_income_payouts():
    res = execute_query("call usp_get_total_income_payouts()")
    return res


def get_total_income(req: GetTotalIncome_Request, match_exact_user_id: bool = False):
    res = execute_query("call usp_get_total_income(_user_id => %s, _match_exact_user_id => %s, _payout_no => %s, _wallet_id => %s, _on_date => %s::timestamptz[], _page_index => %s, _page_size => %s)",
                        (req.user_id, match_exact_user_id, req.payout_no, req.wallet_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.page_index, req.page_size))
    return res


def get_user_total_payout_payment_amount(user_id: str, payout_no: int, wallet_id: int):
    res = execute_query("call usp_get_user_total_payout_payment_amount(_user_id => %s, _payout_no => %s, _wallet_id => %s)",
                        (user_id, payout_no, wallet_id))
    return res


def pay_payout_amount(req: PayPayoutAmount_Request, admin_user_id: str):
    res = execute_query("call usp_pay_payout_amount(_user_id => %s, _payout_no => %s, _wallet_id => %s, _amount => %s, _remarks => %s, _admin_user_id => %s)", (req.user_id, req.payout_no, req.wallet_id, req.amount, req.remarks, admin_user_id))
    return res
