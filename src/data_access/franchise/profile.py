from src.schemas.Franchise import FranchiseOfficeDetailsUpdate_Request, FranchiseOwnerDetailsUpdate_Request, \
    FranchiseLegalDetailsUpdate_Request, FranchiseBankDetailsUpdate_Request
from src.utilities.utils import execute_query


def update_franchise_office_address(req: FranchiseOfficeDetailsUpdate_Request, by_user_id: str, by_user_type: str):

    res = execute_query("call usp_update_franchise_office_details(_user_id => %s, _name => %s, _address => %s, "
                        "_district => %s, _state => %s, _country => %s, _pin_code => %s, _mobile_no => %s, "
                        "_email_id => %s, _by_user_id => %s, _by_user_type => %s)",
                        (req.user_id, req.name, req.address, req.district, req.state, req.country, req.pin_code, req.mobile_no, req.email_id, by_user_id, by_user_type))

    return res


def update_franchise_owner_details(req: FranchiseOwnerDetailsUpdate_Request, by_user_id: str, by_user_type: str):

    res = execute_query("call usp_update_franchise_owner_details(_user_id => %s, _owner_name => %s, _owner_address => %s, _owner_district => %s, "
                        "_owner_state => %s, _owner_country => %s, _owner_pin_code => %s, _owner_mobile_no => %s, "
                        "_owner_email_id => %s, _by_user_id => %s, _by_user_type => %s)",
                        (req.user_id, req.owner_name, req.owner_address, req.owner_district, req.owner_state,
                         req.owner_country, req.owner_pin_code, req.owner_mobile_no, req.owner_email_id, by_user_id, by_user_type))

    return res


def update_franchise_legal_details(req: FranchiseLegalDetailsUpdate_Request, by_user_id: str, by_user_type: str):

    res = execute_query("call usp_update_franchise_legal_details(_user_id => %s, _gstin => %s, _pan_card_no => %s, _pan_card_image => %s, _by_user_id => %s, _by_user_type => %s)",
                        (req.user_id, req.gstin, req.pan_card_no, req.pan_card_image, by_user_id, by_user_type))

    return res


def update_franchise_bank_details(req: FranchiseBankDetailsUpdate_Request, by_user_id: str, by_user_type: str):

    res = execute_query("call usp_update_franchise_bank_details(_user_id => %s, _bank_name => %s, _branch_name => %s, _ifscode => %s, _bank_account_no => %s, _account_holder_name => %s, _upi_id => %s, _by_user_id => %s, _by_user_type => %s)",
                        (req.user_id, req.bank_name, req.branch_name, req.ifscode, req.bank_account_no, req.account_holder_name, req.upi_id, by_user_id, by_user_type))

    return res
