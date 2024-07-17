
from pydantic import BaseModel

from src.misc.constants import VALIDATORS


class AddFranchise_Request(BaseModel):
    franchise_user_id: str = VALIDATORS.USER_ID
    is_master_franchise: bool
    master_franchise_user_id: str
    name: str
    password: str = VALIDATORS.PASSWORD
    address: str
    district: str
    state: int
    country: int
    pin_code: str = VALIDATORS.PIN_CODE
    mobile_no: str = VALIDATORS.MOBILE_NO
    email_id: str = VALIDATORS.EMAIL_ID
    owner_name: str = VALIDATORS.NAME
    owner_address: str
    owner_district: str
    owner_state: int
    owner_country: int
    owner_pin_code: str = VALIDATORS.PIN_CODE
    owner_mobile_no: str = VALIDATORS.MOBILE_NO
    owner_email_id: str = VALIDATORS.EMAIL_ID
    gstin: str = VALIDATORS.GSTIN
    pan_card_no: str = VALIDATORS.PAN_CARD_NUMBER
    pan_card_image: str
    bank_name: str
    branch_name: str
    ifscode: str = VALIDATORS.IFSCODE
    bank_account_no: str = VALIDATORS.BANK_ACCOUNT_NUMBER
    account_holder_name: str = VALIDATORS.NAME
    upi_id: str = VALIDATORS.UPI_ID


class FranchiseList_Request(BaseModel):
    master_franchise_user_id: str = ''
    franchise_id_name_email_mobile: str = ''
    joining_date_from: str = ''
    joining_date_to: str = ''
    page_index: int
    page_size: int


class FranchiseAccessRightsUpdateRequest(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    access_rights: str = VALIDATORS.ACCESS_RIGHTS


class FranchiseOfficeDetailsUpdate_Request(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    name: str
    address: str
    district: str
    state: int
    country: int
    pin_code: str = VALIDATORS.PIN_CODE
    mobile_no: str = VALIDATORS.MOBILE_NO
    email_id: str = VALIDATORS.EMAIL_ID


class FranchiseOwnerDetailsUpdate_Request(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    owner_name: str = VALIDATORS.NAME
    owner_address: str
    owner_district: str
    owner_state: int
    owner_country: int
    owner_pin_code: str = VALIDATORS.PIN_CODE
    owner_mobile_no: str = VALIDATORS.MOBILE_NO
    owner_email_id: str = VALIDATORS.EMAIL_ID


class FranchiseLegalDetailsUpdate_Request(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    gstin: str = VALIDATORS.GSTIN
    pan_card_no: str = VALIDATORS.PAN_CARD_NUMBER
    pan_card_image: str


class FranchiseBankDetailsUpdate_Request(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    bank_name: str
    branch_name: str
    ifscode: str = VALIDATORS.IFSCODE
    bank_account_no: str = VALIDATORS.BANK_ACCOUNT_NUMBER
    account_holder_name: str = VALIDATORS.NAME
    upi_id: str = VALIDATORS.UPI_ID


class GetFranchiseProducts_Request(BaseModel):
    franchise_id: str=''
    product_id: int=0
    category_id: int=0
    name: str = ''
    date_from: str=''
    date_to: str=''
    page_index: int
    page_size: int


class GetFranchiseProductStockTransactions_Request(BaseModel):
    franchise_id: str=''
    product_id: int=0
    category_id: int=0
    date_from: str=''
    date_to: str=''
    page_index: int
    page_size: int
