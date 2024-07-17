from src.schemas.Income import GetRepurchaseLevelIncome_Request
from src.utilities.utils import execute_query


def get_repurchase_level_income(req: GetRepurchaseLevelIncome_Request, match_exact_user_id: bool = False):
    res = execute_query("call usp_get_repurchase_level_income(_user_id => %s, _match_exact_user_id => %s, _downline_id => %s, _level => %s, _on_date => %s::timestamptz[], _page_index => %s, _page_size => %s)",
                        (req.user_id, match_exact_user_id, req.downline_id, req.level, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.page_index, req.page_size))
    return res
