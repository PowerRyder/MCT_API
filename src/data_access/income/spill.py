
from src.schemas.Income import GetSpillIncome_Request
from src.utilities.utils import execute_query


def get_spill_income(req: GetSpillIncome_Request, match_exact_user_id: bool = False):
    res = execute_query("call usp_get_spill_income(_user_id => %s, _match_exact_user_id => %s, _from_user_id => %s, _on_date => %s::timestamptz[], _type => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, match_exact_user_id, req.from_user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.type, req.page_index, req.page_size))
    return res
