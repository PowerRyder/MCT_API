from src.schemas.Repurchase import AddCategory_Request, GetCategories_Request, UpdateCategory_Request
from src.utilities.utils import execute_query


def add_category(req: AddCategory_Request, added_by_admin_id: str):
    res = execute_query(
        "call usp_add_repurchase_product_category(_parent_id => %s, _name => %s, _can_have_subcategories => %s, _added_by_admin_id => %s)",
        (req.parent_id, req.name, req.can_have_subcategories, added_by_admin_id))
    return res


def get_categories(req: GetCategories_Request):
    res = execute_query(
        "call usp_get_repurchase_product_categories(_name => %s, _between_date => %s::timestamptz[], _parent_id => %s, _all => %s, _page_index => %s, _page_size => %s)",
        (req.name, [req.date_from if req.date_from != '' else None, req.date_to if req.date_to != '' else None],
         req.parent_id, req.all, req.page_index, req.page_size))
    return res


def update_category(req: UpdateCategory_Request, admin_user_id: str):
    res = execute_query(
        "call usp_update_repurchase_product_category(_category_id => %s, _name => %s, _parent_id => %s, _updated_by_admin_id => %s)",
        (req.category_id, req.name, req.parent_id, admin_user_id))
    return res


def delete_category(category_id: int, admin_user_id: str):
    res = execute_query("call usp_delete_repurchase_category(_category_id => %s, _by_admin_user_id => %s)",
                        (category_id, admin_user_id))
    return res
