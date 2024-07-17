from src.schemas.Franchise import GetFranchiseProductStockTransactions_Request, GetFranchiseProducts_Request
from src.utilities.utils import execute_query


def get_franchise_products(req: GetFranchiseProducts_Request, match_exact_user_id: bool):
    res = execute_query(
        "call usp_get_franchise_repurchase_products(_franchise_id => %s, _match_exact_user_id => %s, _product_id => %s, _category_id => %s, _name => %s, _between_date => %s::timestamptz[], _page_index => %s, _page_size => %s)",
        (req.franchise_id, match_exact_user_id, req.product_id, req.category_id, req.name, [req.date_from if req.date_from != '' else None, req.date_to if req.date_to != '' else None], req.page_index, req.page_size))
    return res


def get_franchise_product_stock_transactions(req: GetFranchiseProductStockTransactions_Request, match_exact_user_id: bool):
    res = execute_query(
        "call usp_get_franchise_repurchase_product_transactions(_franchise_id => %s, _match_exact_user_id => %s, _product_id => %s, _category_id => %s, _between_date => %s::timestamptz[], _page_index => %s, _page_size => %s)",
        (req.franchise_id, match_exact_user_id, req.product_id, req.category_id, [req.date_from if req.date_from != '' else None, req.date_to if req.date_to != '' else None], req.page_index, req.page_size))
    return res
