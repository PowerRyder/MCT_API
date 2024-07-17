from src.schemas.Income import UpdateROIPercentage_Request
from src.utilities.utils import execute_query


def get_roi_ranks():
    res = execute_query("call usp_get_roi_ranks()")
    return res


def update_roi_rank_percentage(req: UpdateROIPercentage_Request, user_id: str):
    res = execute_query("call usp_update_package_roi_percentage(_package_id => %s, _roi_percentage => %s, _by_admin_user_id => %s)", (req.rank_id, req.percentage, user_id))
    return res


def process_roi(admin_id: str):
    res = execute_query("call usp_process_roi_income(_by_admin_id => %s)", (admin_id, ))
    return res
