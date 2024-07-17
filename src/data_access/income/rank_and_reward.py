from src.schemas.Income import GetRankAndRewardIncome_Request
from src.utilities.utils import execute_query


def get_ranks():
    res = execute_query("call usp_get_ranks()")
    return res


def get_rank_and_reward_income(req: GetRankAndRewardIncome_Request, match_exact_user_id: bool = False):
    res = execute_query("call usp_get_rank_and_reward_income(_user_id => %s, _match_exact_user_id => %s, _on_date => %s::timestamptz[], _rank_id => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, match_exact_user_id, [req.date_from if req.date_from != '' else None, req.date_to if req.date_to != '' else None], req.rank_id, req.page_index, req.page_size))
    return res
