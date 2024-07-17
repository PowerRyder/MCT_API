
from src.schemas.Income import GetReferralIncome_Request
from src.utilities.utils import execute_query


def get_referral_income(req: GetReferralIncome_Request, match_exact_user_id: bool = False):
    res = execute_query("call usp_get_referral_income(_user_id => %s, _match_exact_user_id => %s, _from_user_id => %s, _on_date => %s::timestamptz[], _page_index => %s, _page_size => %s)", 
                        (req.user_id, match_exact_user_id, req.from_user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.page_index, req.page_size))
    return res
