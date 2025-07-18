
from src.schemas.Income import GetROILevelIncome_Request, GetRoiIncome_Request, UpdateROIPercentage_Request
from src.utilities.utils import execute_query


def get_roi_income(req: GetRoiIncome_Request, match_exact_user_id: bool = False):
    res = execute_query("call usp_get_roi_income(_user_id => %s, _match_exact_user_id => %s, _on_date => %s::timestamptz[], _package_id => %s, _page_index => %s, _page_size => %s)", 
                        (req.user_id, match_exact_user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.package_id, req.page_index, req.page_size))
    return res


def get_roi_level_income(req: GetROILevelIncome_Request, match_exact_user_id: bool = False):
    res = execute_query("call usp_get_roi_level_income(_user_id => %s, _match_exact_user_id => %s, _downline_id => %s, _level => %s, _on_date => %s::timestamptz[], _package_id => %s, _roi_id => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, match_exact_user_id, req.downline_id, req.level, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.package_id, req.roi_id, req.page_index, req.page_size))
    return res


def get_roi_level_income_concise(user_id: str):
    res = execute_query("call usp_get_roi_level_income_concise(_user_id => %s)", (user_id, ))
    return res

