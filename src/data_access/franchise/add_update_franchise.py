from src.schemas.Franchise import AddFranchise_Request, FranchiseList_Request
from src.utilities.utils import execute_query


def add_franchise(req: AddFranchise_Request, added_by_user_id: str, added_by_user_type: str):

    res = execute_query("call usp_add_franchise(_franchise_user_id => %s, _is_master_franchise => %s, "
                        "_master_franchise_user_id => %s, _name => %s, _password => %s, _address => %s, "
                        "_district => %s, _state => %s, _country => %s, _pin_code => %s, _mobile_no => %s, "
                        "_email_id => %s, _owner_name => %s, _owner_address => %s, _owner_district => %s, "
                        "_owner_state => %s, _owner_country => %s, _owner_pin_code => %s, _owner_mobile_no => %s, "
                        "_owner_email_id => %s, _gstin => %s, _pan_card_no => %s, _pan_card_image => %s, "
                        "_bank_name => %s, _branch_name => %s, _ifscode => %s, _bank_account_no => %s, "
                        "_account_holder_name => %s, _upi_id => %s, _added_by_user_id => %s, _added_by_user_type => %s)",
                        (req.franchise_user_id, req.is_master_franchise, req.master_franchise_user_id, req.name,
                         req.password, req.address, req.district, req.state, req.country, req.pin_code, req.mobile_no,
                         req.email_id, req.owner_name, req.owner_address, req.owner_district, req.owner_state,
                         req.owner_country, req.owner_pin_code, req.owner_mobile_no, req.owner_email_id, req.gstin,
                         req.pan_card_no, req.pan_card_image, req.bank_name, req.branch_name, req.ifscode,
                         req.bank_account_no, req.account_holder_name, req.upi_id, added_by_user_id, added_by_user_type))

    return res


def get_franchise_list(req: FranchiseList_Request):
    res = execute_query(
        "call usp_get_franchise(_master_franchise_user_id => %s, _franchise_id_name_email_mobile => %s, _joining_date => %s::timestamptz[], _page_index => %s, _page_size => %s)",
        (req.master_franchise_user_id, req.franchise_id_name_email_mobile, [req.joining_date_from if req.joining_date_from != '' else None, req.joining_date_to if req.joining_date_to != '' else None], req.page_index, req.page_size))
    return res


def toggle_franchise_block_unblock(user_id: str, by_user_id: str):
    res = execute_query("call usp_toggle_franchise_block_unblock(_user_id => %s, _by_user_id => %s)",
                        (user_id, by_user_id))
    return res


def get_master_franchise_access_rights_for_admin():
    res = execute_query("call usp_get_master_franchise_access_rights_for_admin()")
    return res


def update_franchise_access_rights(user_id, access_rights, by_user_id, by_user_type):
    res = execute_query(
        "call usp_update_franchise_access_rights(_user_id => %s, _access_rights => %s, _by_user_id => %s, _by_user_type => %s)",
        (user_id, access_rights, by_user_id, by_user_type))
    return res

