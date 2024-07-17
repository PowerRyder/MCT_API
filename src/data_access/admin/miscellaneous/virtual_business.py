
from src.schemas.VirtualBusiness import AddVirtualBusinessRequest, GetVirtualBusinessRequest
from src.utilities.utils import execute_query


def insert_virtual_business(req: AddVirtualBusinessRequest, admin_user_id: str):
    res = execute_query("call usp_insert_virtual_business(_user_id => %s, _binary_type_id => %s, _amount => %s, _point_value => %s, _side => %s, _by_admin_user_id => %s, _remarks => %s)",
    (req.user_id, req.binary_type_id, req.amount, req.point_value, req.side, admin_user_id, req.remarks))
    return res

def get_virtual_business(req: GetVirtualBusinessRequest, match_exact_user_id: bool):
    res = execute_query("call usp_get_virtual_business_details(_user_id => %s, _match_exact_user_id => %s, _date_range => %s::timestamptz[], _binary_type_id => %s, _page_index => %s, _page_size => %s)",
    (req.user_id, match_exact_user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.binary_type_id, req.page_index, req.page_size))
    return res


def get_total_matching_business(user_id: str, binary_type_id: int):
    res = execute_query("call usp_get_total_matching_business(_user_id => %s, _binary_type_id => %s)", (user_id, binary_type_id))
    return res
