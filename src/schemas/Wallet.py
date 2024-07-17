
from pydantic import BaseModel

from src.misc.constants import VALIDATORS

class WalletBalanceRequest(BaseModel):
    user_id: str = ''
    user_type: str = VALIDATORS.USER_TYPE
    wallet_id: int = 0
    page_index: int = 0
    page_size: int = 100

class WalletTransactionsRequest(BaseModel):
    user_id: str
    user_type: str = VALIDATORS.USER_TYPE
    date_from: str=''
    date_to: str=''
    wallet_id: int = 0
    type: str='All'
    search_term: str=''
    page_index: int
    page_size: int
    
class WalletCreditDebit(BaseModel):
    user_id: str
    user_type: str = VALIDATORS.USER_TYPE
    wallet_id: int = 0
    action: str = VALIDATORS.CREDIT_DEBIT_ACTION
    amount: float
    remarks: str = ''
    
class WalletTransferFund(BaseModel):
    from_user_id: str
    from_user_type: str = VALIDATORS.USER_TYPE
    from_wallet_id: int
    to_user_id: str
    to_user_type: str = VALIDATORS.USER_TYPE
    to_wallet_id: int
    amount: float
    remarks: str = ''
    two_factor_auth_request_id: str = ''
    
class TransferFundHistoryRequest(BaseModel):
    is_from: bool = True
    from_user_id: str = ''
    from_user_type: str = VALIDATORS.USER_TYPE_ALL
    from_wallet_id: int = 0
    to_user_id: str = ''
    to_user_type: str = VALIDATORS.USER_TYPE_ALL
    to_wallet_id: int = 0
    date_from: str = ''
    date_to: str = ''
    remarks: str = ''
    page_index: int
    page_size: int
    
    
class RequestForCredit(BaseModel):
    wallet_id: int
    amount: float
    payment_request_id: str = VALIDATORS.REQUIRED
    
class GetCreditRequests(BaseModel):
    user_id: str
    user_type: str = VALIDATORS.USER_TYPE_ALL
    date_from: str=''
    date_to: str=''
    payment_mode: str=''
    reference_number: str=''
    status: str='All'
    page_index: int
    page_size: int

class CreditRequestApproveRejectDataItem(BaseModel):
    RequestId: int
    Remarks: str = ''
    Status: str = VALIDATORS.STATUS_APPROVED_REJECTED
