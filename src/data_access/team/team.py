
from src.schemas.TeamDetails import DayWiseBusinessDetailsRequest, DirectDetailsRequest, DownlineDetailsRequest
from src.utilities.utils import execute_query


def getDirectDetails(req: DirectDetailsRequest):
    res = execute_query("call usp_get_directs(_sponsor_id => %s, _direct_id_name_email_mobile => %s, _joining_date => %s::timestamptz[], _side => %s, _active_status => %s, _page_index => %s, _page_size => %s)", 
    (req.sponsor_id, req.direct_id_name_email_mobile, [req.joining_date_from if req.joining_date_from!='' else None, req.joining_date_to if req.joining_date_to!='' else None], req.side, req.active_status, req.page_index, req.page_size))
    return res
    
def getDownlineDetails(req: DownlineDetailsRequest):
    res = execute_query("call usp_get_downline(_user_id => %s, _downline_id_name_email_mobile => %s, _joining_date => %s::timestamptz[], _side => %s, _active_status => %s, _level => %s, _page_index => %s, _page_size => %s)", 
    (req.user_id, req.downline_id_name_email_mobile, [req.joining_date_from if req.joining_date_from!='' else None, req.joining_date_to if req.joining_date_to!='' else None], req.side, req.active_status, req.level, req.page_index, req.page_size))
    return res
    
def getDayWiseBusinessDetails(req: DayWiseBusinessDetailsRequest):
    res = execute_query("call usp_get_business_details_day_wise(_user_id => %s, _between_date => %s::timestamptz[], _page_index => %s, _page_size => %s)", 
    (req.user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.page_index, req.page_size))
    return res
    