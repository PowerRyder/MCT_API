from src.schemas.Repurchase import AddProductStock_Request, GetProductStockTransactions_Request
from src.utilities.utils import execute_query


def add_product_stock(req: AddProductStock_Request, added_by_admin_id: str):
    res = execute_query(
        "call usp_add_repurchase_product_stock(_product_id => %s, _qty => %s, _by_admin_id => %s, _remarks => %s)",
        (req.product_id, req.quantity, added_by_admin_id, req.remarks))
    return res


def get_product_stock_transactions(req: GetProductStockTransactions_Request):
    res = execute_query(
        "call usp_get_repurchase_product_transactions(_product_id => %s, _category_id => %s, _remarks => %s, _between_date => %s::timestamptz[], _page_index => %s, _page_size => %s)",
        (req.product_id, req.category_id, req.remarks, [req.date_from if req.date_from != '' else None, req.date_to if req.date_to != '' else None], req.page_index, req.page_size))
    return res
