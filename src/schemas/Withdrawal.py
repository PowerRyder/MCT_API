
from pydantic import BaseModel

from src.misc.constants import VALIDATORS


class WithdrawFund(BaseModel):
    wallet_id: int
    crypto_network: str = ''
    token_symbol: str = ''
    token_type: str = ''
    crypto_wallet_address: str = ''
    amount: float
    remarks: str = ''
    two_factor_auth_request_id: str = ''
    
class GetWithdrawalRequests(BaseModel):
    user_id: str
    user_type: str = VALIDATORS.USER_TYPE_ALL
    date_from: str=''
    date_to: str=''
    status: str='All'
    page_index: int
    page_size: int

class WithdrawalRequestApproveRejectDataItem(BaseModel):
    RequestId: int
    Remarks: str = ''
    Status: str = VALIDATORS.STATUS_APPROVED_REJECTED
