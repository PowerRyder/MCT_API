import json

from src.schemas.Repurchase import AddShippingAddress, PlaceRepurchaseOrder, GetRepurchaseOrders, \
    RepurchaseOrderDispatchStatusUpdateRequest
from src.utilities.utils import execute_query


def get_shipping_addresses(user_id: str, user_type: str):
    res = execute_query(
        "call usp_get_shipping_addresses(_user_id => %s, _user_type => %s)", (user_id, user_type))
    return res


def add_shipping_address(req: AddShippingAddress, added_by_id: str, add_by_user_type: str):
    res = execute_query(
        "call usp_add_shipping_address(_user_id => %s, _user_type => %s, _name => %s, _address => %s, _district => %s, "
        "_state => %s, _country => %s, _pin_code => %s, _mobile_no => %s, _added_by_user_id => %s, _added_by_user_type => %s)",
        (req.user_id, req.user_type, req.name, req.address, req.district, req.state, req.country, req.pin_code, req.mobile_no, added_by_id, add_by_user_type))
    return res


def place_repurchase_order(req: PlaceRepurchaseOrder, by_id: str, by_user_type: str):
    res = execute_query(
        "call usp_place_repurchase_order(_to_user_id => %s, _to_user_type => %s, _by_user_id => %s, _by_user_type => %s, _shipping_charges => %s, "
        "_products => %s::jsonb, _payment_id => %s, _is_paid => %s, _is_dispatched => %s, _dispatch_mode => %s, _courier_name => %s, _courier_url => %s, "
        "_courier_tracking_number => %s, _shipping_address_id => %s, _wallet_id => %s)",
        (
            req.to_user_id, req.to_user_type, by_id, by_user_type, req.shipping_charges, json.dumps(req.products), int(req.payment_id), req.is_paid, req.is_dispatched,
            req.dispatch_mode, req.courier_name, req.courier_url, req.courier_tracking_number, req.shipping_address_id, req.wallet_id
        ))
    return res


def get_repurchase_orders(req: GetRepurchaseOrders, match_exact_user_id: bool, match_exact_franchise_id: bool, do_not_include_self_orders: bool):
    res = execute_query(
        "call usp_get_repurchase_orders(_order_number => %s,"
        "_user_id => %s, _match_exact_user_id => %s, _user_type => %s, _by_franchise_id => %s, _match_exact_franchise_id => %s, "
        "_between_date => %s::timestamptz[], _payment_mode => %s, _reference_no => %s, _dispatch_status => %s, _paid_status => %s, _do_not_include_self_orders => %s, _order_id => %s, _page_index => %s, _page_size => %s)",
        (
            req.order_number, req.user_id, match_exact_user_id, req.user_type, req.by_franchise_id, match_exact_franchise_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None],
            req.payment_mode, req.reference_no, req.dispatch_status, req.paid_status, do_not_include_self_orders, req.order_id, req.page_index, req.page_size
        ))
    return res


def get_repurchase_order_details(order_id: int, page_index: int, page_size: int):
    res = execute_query(
        "call usp_get_repurchase_order_details(_order_id => %s, _page_index => %s, _page_size => %s)", (order_id, page_index, page_size))
    return res


def mark_order_as_paid(order_id: int, by_id: str, by_user_type: str):
    res = execute_query(
        "call usp_mark_repurchase_order_as_paid(_order_id => %s, _by_user_id => %s, _by_user_type => %s)", (order_id, by_id, by_user_type))
    return res


def update_order_dispatch_status(req: RepurchaseOrderDispatchStatusUpdateRequest, by_user_id: str, by_user_type: str):
    res = execute_query("call usp_dispatch_or_reject_repurchase_order(_order_id => %s, _status => %s, _dispatch_mode => %s, _courier_name => %s, _courier_url => %s, _courier_tracking_number => %s, _remarks => %s, _by_user_id => %s, _by_user_type => %s)",
                        (req.order_id, req.status, req.dispatched_through, req.courier_name, req.courier_url, req.courier_tracking_number, req.remarks, by_user_id, by_user_type))
    return res
