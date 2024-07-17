from src.schemas.Income import GetWeeklyBonusIncome_Request
from src.utilities.utils import execute_query


def get_weekly_bonus_payouts():
    res = execute_query("call usp_get_weekly_bonus_payouts()")
    return res


def get_weekly_bonus_income(req: GetWeeklyBonusIncome_Request, match_exact_user_id: bool = False):
    res = execute_query("call usp_get_weekly_bonus_income(_user_id => %s, _match_exact_user_id => %s, _payout_no => %s, _between_date => %s::timestamptz[], _page_index => %s, _page_size => %s)",
                        (req.user_id, match_exact_user_id, req.payout_no, [req.date_from if req.date_from != '' else None, req.date_to if req.date_to != '' else None], req.page_index, req.page_size))
    return res
