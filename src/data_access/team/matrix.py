from src.schemas.TeamDetails import GetMatrixMembers
from src.utilities.utils import execute_query


def get_pools():
    res = execute_query(
        "call usp_get_matrices()")
    return res


def get_pool_entry_ids(user_id: str, pool_id: int):
    res = execute_query("call usp_get_matrix_entry_ids(_user_id => %s, _pool_id => %s)", (user_id, pool_id))
    return res

def get_matrix_members(req: GetMatrixMembers):
    res = execute_query("call usp_get_matrix_members(_user_id => %s, _pool_id => %s, _matrix_id => %s, _downline_user_id => %s, _between_date => %s::timestamptz[], _level => %s, _page_index => %s, _page_size => %s)",
    (req.user_id, req.pool_id, req.matrix_id, req.downline_user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.level, req.page_index, req.page_size))
    return res