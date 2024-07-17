
from src.schemas.Income import GetMatrixIncome_Request
from src.utilities.utils import execute_query


def get_matrix_income(req: GetMatrixIncome_Request, match_exact_user_id: bool = False):
    res = execute_query("call usp_get_matrix_income(_user_id => %s, _match_exact_user_id => %s, _downline_id => %s, _level => %s, _on_date => %s::timestamptz[], _matrix_id => %s, _pool_id => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, match_exact_user_id, req.downline_id, req.level, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.matrix_id, req.pool_id, req.page_index, req.page_size))
    return res

def get_matrix_income_concise(user_id: str, pool_id: int, matrix_id: int):
    res = execute_query("call usp_get_matrix_income_concise(_user_id => %s, _pool_id => %s, _matrix_id => %s)", (user_id, pool_id, matrix_id))
    return res
