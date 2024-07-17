
from pydantic import BaseModel
from src.misc.constants import VALIDATORS

class PinGenerateRequest(BaseModel):
    to_user_id: str = VALIDATORS.USER_ID
    to_user_type: str = VALIDATORS.USER_TYPE
    package_id: int
    pin_value: float
    pin_value_paid: float
    wallet_id: int
    no_of_pins: int
    generation_user_remarks: str
    two_factor_auth_request_id: str


class ViewPinRequest(BaseModel):
    user_id: str
    user_type: str = VALIDATORS.USER_TYPE_ALL
    package_id: int=0
    date_from: str=''
    date_to: str=''
    used_status: str
    pin_generate_request_id: int
    pin_transfer_request_id: int
    pin_request_id: int
    page_index: int
    page_size: int


class PayPartialPinAmountRequest(BaseModel):
    pinNumber: int
    pinPassword: int
    amount: float
    remarks: str


class PinStatisticsRequest(BaseModel):
    user_id: str
    user_type: str = VALIDATORS.USER_TYPE_ALL
    package_id: int=0
    date_from: str=''
    date_to: str=''
    page_index: int
    page_size: int
    

class PinTransferRequest(BaseModel):
    from_user_id: str = VALIDATORS.USER_ID
    to_user_id: str = VALIDATORS.USER_ID
    package_id: int
    no_of_pins: int
    remarks: str
    two_factor_auth_request_id: str = ''


class PinTransferHistoryRequest(BaseModel):
    type: str = VALIDATORS.TRANSFER_TYPE
    from_user_id: str
    from_user_type: str = VALIDATORS.USER_TYPE_ALL
    to_user_id: str
    to_user_type: str = VALIDATORS.USER_TYPE_ALL
    package_id: int=0
    date_from: str=''
    date_to: str=''
    page_index: int
    page_size: int


class PinRequest(BaseModel):
    payment_request_id: str = VALIDATORS.REQUIRED
    pins=[]


class GetPinRequest(BaseModel):
    user_id: str
    user_type: str = VALIDATORS.USER_TYPE_ALL
    date_from: str=''
    date_to: str=''
    payment_mode: str=''
    reference_number: str=''
    status: str='All'
    page_index: int
    page_size: int


class PinRequestApproveRejectDataItem(BaseModel):
    RequestId: int
    Remarks: str = ''
    Status: str = VALIDATORS.STATUS_APPROVED_REJECTED


class PinProductDispatchDetailsRequest(BaseModel):
    user_id: str
    package_id: int = 0
    date_from: str = ''
    date_to: str = ''
    status: str = VALIDATORS.PIN_PRODUCT_DISPATCH_STATUS_ALL
    by_user_id: str
    by_user_type: str = VALIDATORS.USER_TYPE_ALL
    page_index: int
    page_size: int


class PinProductDispatchStatusUpdateRequest(BaseModel):
    pin_srno: int
    status: str = VALIDATORS.PIN_PRODUCT_DISPATCH_STATUS_UPDATE
    dispatched_through: str
    dispatch_date: str
    courier_name: str
    courier_url: str
    courier_tracking_number: str
    remarks: str = ''
