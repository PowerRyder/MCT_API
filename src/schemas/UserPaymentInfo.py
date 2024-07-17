
from fastapi import File, UploadFile
from pydantic import BaseModel
from src.misc.constants import VALIDATORS


class UserBankDetailsUpdateRequest(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    bank_name: str
    branch_name: str
    ifscode: str = VALIDATORS.IFSCODE
    bank_account_no: str = VALIDATORS.BANK_ACCOUNT_NUMBER
    account_holder_name: str = VALIDATORS.NAME

class UserUpiDetailsUpdateRequest(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    upi_id: str = VALIDATORS.UPI_ID
    
class UserCryptoWithdrawalAddressRequest(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    crypto_id: int = VALIDATORS.REQUIRED
    address: str = VALIDATORS.REQUIRED
    