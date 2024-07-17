from src.schemas.Repurchase import AddCategory_Request, GetCategories_Request, UpdateCategory_Request, \
    AddUpdateProduct_Request, GetProducts_Request
from src.utilities.utils import execute_query


def add_or_update_product(req: AddUpdateProduct_Request, added_by_admin_id: str):
    res = execute_query(
        "call usp_add_or_update_repurchase_product(_product_id => %s, _product_name => %s, _product_image => %s, _category_id => %s, _hsn => %s, _bv => %s, _mrp => %s, "
        "_discount_percentage => %s, _gst_percentage => %s, _description => %s, _added_by_admin_id => %s)",
        (req.product_id, req.product_name, req.product_image, req.category_id, req.hsn, req.bv, req.mrp, req.discount_percentage, req.gst_percentage, req.description, added_by_admin_id))
    return res


def get_products(req: GetProducts_Request):
    res = execute_query(
        "call usp_get_repurchase_products(_product_id => %s, _category_id => %s, _name => %s, _between_date => %s::timestamptz[], _page_index => %s, _page_size => %s)",
        (req.product_id, req.category_id, req.name, [req.date_from if req.date_from != '' else None, req.date_to if req.date_to != '' else None], req.page_index, req.page_size))
    return res


def delete_product(product_id: int, admin_user_id: str):
    res = execute_query("call usp_delete_repurchase_product(_product_id => %s, _by_admin_user_id => %s)",
                        (product_id, admin_user_id))
    return res
