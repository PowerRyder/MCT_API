from src.schemas.Income import GetMatchingIncome_Request, GetMatchingBusinessDetails_Request, \
    GetMatchingLevelIncome_Request
from src.utilities.utils import execute_query


def get_matching_payouts():
    res = execute_query("call usp_get_matching_payouts()")
    return res


def get_matching_types():
    res = execute_query("call usp_get_matching_types()")
    return res


def get_matching_income(req: GetMatchingIncome_Request, match_exact_user_id: bool = False):
    res = execute_query("call usp_get_matching_income(_user_id => %s, _match_exact_user_id => %s, _payout_no => %s, _on_date => %s::timestamptz[], _binary_type_id => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, match_exact_user_id, req.payout_no, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.binary_type_id, req.page_index, req.page_size))
    return res


def get_matching_business_details(req: GetMatchingBusinessDetails_Request):
    res = execute_query("call usp_get_matching_business_details(_user_id => %s, _payout_no => %s, _binary_type_id => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, req.payout_no, req.binary_type_id, req.page_index, req.page_size))
    return res


def get_matching_level_income(req: GetMatchingLevelIncome_Request, match_exact_user_id: bool = False):
    res = execute_query("call usp_get_matching_level_income(_user_id => %s, _match_exact_user_id => %s, _downline_id => %s, _level => %s, _on_date => %s::timestamptz[], _payout_no => %s, _binary_type_id => %s, _binary_income_id => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, match_exact_user_id, req.downline_id, req.level, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.payout_no, req.binary_type_id, req.binary_income_id, req.page_index, req.page_size))
    return res


def get_matching_level_income_concise(user_id: str, payout_no: int, binary_type_id: int):
    res = execute_query("call usp_get_matching_level_income_concise(_user_id => %s, _payout_no => %s, _binary_type_id => %s)", (user_id, payout_no, binary_type_id))
    return res
