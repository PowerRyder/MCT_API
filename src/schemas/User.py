
from pydantic import BaseModel
from src.misc.constants import VALIDATORS


class UserPersonalDetailsUpdateRequest(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    name: str = VALIDATORS.NAME
    dob: str = VALIDATORS.REQUIRED
    gender: str = VALIDATORS.GENDER
    marital_status: str = VALIDATORS.MARITAL_STATUS
    
class UserContactDetailsUpdateRequest(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    email_id: str = VALIDATORS.EMAIL_ID
    mobile_no: str = VALIDATORS.MOBILE_NO
    address: str = VALIDATORS.DEFAULT
    district: str = VALIDATORS.DEFAULT
    pin_code: str = VALIDATORS.PIN_CODE
    country: int
    state: int
    two_factor_auth_request_id: str = ''
    
class UserNomineeDetailsUpdateRequest(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    nominee_title: str = VALIDATORS.TITLE
    nominee_name: str = VALIDATORS.NAME
    nominee_relationship: str = VALIDATORS.NOMINEE_RELATIONSHIP
    