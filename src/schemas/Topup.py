
from pydantic import BaseModel
from src.misc.constants import VALIDATORS


class TopupByPinRequest(BaseModel):
    userId: str=VALIDATORS.USER_ID
    pinNumber: int=0
    pinPassword: int=0
    remarks: str=''
    two_factor_auth_request_id: str = ''

class TopupFromWalletRequest(BaseModel):
    user_id: str=VALIDATORS.USER_ID
    package_id: int=0
    pin_value: float=0
    pin_value_paid: float=0
    wallet_id: int=0
    remarks: str=''
    two_factor_auth_request_id: str = ''

class TopupDetailsRequest(BaseModel):
    topup_for: str = VALIDATORS.TOPUP_FOR
    user_id: str = ''
    topup_date_from: str = ''
    topup_date_to: str = ''
    side: str = 'All'
    level: int = 0
    package_id: int = 0
    topup_type: str = 'All'
    by_user_id: str = ''
    by_user_type: str = VALIDATORS.USER_TYPE_ALL
    pin_number: int = 0
    page_index: int = 0
    page_size: int = 100

class RoiBlockUnblockRequest(BaseModel):
    pin_srno: int
    status: str = VALIDATORS.ROI_BLOCK_STATUS
    remarks: str=''


class GetCryptoDeposit(BaseModel):
    user_id: str = ''
    date_from: str = ''
    date_to: str = ''
    request_id = ''
    txn_hash: str = ''
    input_txn_status: str = 'All'
    page_index: int = 0
    page_size: int = 100
