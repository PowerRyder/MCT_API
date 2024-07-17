
from src.schemas.Pin import PinProductDispatchDetailsRequest, PinProductDispatchStatusUpdateRequest
from src.utilities.utils import execute_query


def get_pin_product_dispatch_details(req: PinProductDispatchDetailsRequest, match_exact_user_id: bool):
    res = execute_query("call usp_get_pin_product_dispatch_details(_user_id => %s, _match_exact_user_id => %s, _package_id => %s, _between_date => %s::timestamptz[], _dispatch_status => %s, _by_user_id => %s, _by_user_type => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, match_exact_user_id, req.package_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.status, req.by_user_id, req.by_user_type, req.page_index, req.page_size))
    return res

def update_pin_product_dispatch_status(req: PinProductDispatchStatusUpdateRequest, by_user_id: str, by_user_type: str):
    res = execute_query("call usp_update_pin_product_dispatch_status(_pin_srno => %s, _status => %s, _dispatched_through => %s, _dispatch_date => %s::timestamptz, _courier_name => %s, _courier_url => %s, _courier_tracking_number => %s, _remarks => %s, _by_user_id => %s, _by_user_type => %s)",
                        (req.pin_srno, req.status, req.dispatched_through, req.dispatch_date, req.courier_name, req.courier_url, req.courier_tracking_number, req.remarks, by_user_id, by_user_type))
    return res
