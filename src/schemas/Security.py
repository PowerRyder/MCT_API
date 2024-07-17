
from pydantic import BaseModel

from src.misc.constants import VALIDATORS


class TwoFactorAuthenticationRequest(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    request_id: str = VALIDATORS.TWO_FACTOR_AUTH_REQUEST_ID
    mode: str = VALIDATORS.TWO_FACTOR_AUTH_MODE
    code: str = VALIDATORS.OTP
    

class ChangePassword(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    user_type: str = VALIDATORS.USER_TYPE
    old_password: str = VALIDATORS.PASSWORD
    new_password: str = VALIDATORS.PASSWORD
    two_factor_auth_request_id: str = ''

class ChangePasswordByAdmin(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    new_password: str = VALIDATORS.PASSWORD
