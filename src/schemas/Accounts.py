
from typing import Optional
from pydantic import BaseModel
from src.utilities.utils import company_details
from src.misc.constants import VALIDATORS


class Register(BaseModel):
    userId: Optional[str] = VALIDATORS.USER_ID
    password: str = VALIDATORS.PASSWORD
    confirmPassword: str = VALIDATORS.PASSWORD

    if company_details['is_pin_paid_registration']:
        pinNumber: int = 0
        pinPassword: int = 0

    referralId: str = ''

    if company_details['is_binary_system']:
        side: str = VALIDATORS.SIDE

        # if(company_details['is_upline_registration']):
        uplineId: Optional[str] = VALIDATORS.USER_ID

    name: Optional[str] = VALIDATORS.NAME
    dob: Optional[str] = None
    maritalStatus: Optional[str] = VALIDATORS.MARITAL_STATUS
    gender: Optional[str] = VALIDATORS.GENDER
    address: Optional[str] = ''
    district: Optional[str] = ''
    state: Optional[int] = 0
    country: Optional[int] = 0
    pincode: Optional[str] = VALIDATORS.PIN_CODE
    mobile: str = VALIDATORS.MOBILE_NO
    email: str = VALIDATORS.EMAIL_ID

    if company_details['is_nominee_registration']:
        nomineeTitle: str = VALIDATORS.TITLE
        nomineeName: str = VALIDATORS.NAME
        nomineeRelationship: str = VALIDATORS.NOMINEE_RELATIONSHIP

    if company_details['is_bank_info_registration']:
        bankName: str = ''
        branchName: str = ''
        IFSCode: str = VALIDATORS.IFSCODE
        bankAccountNumber: str = VALIDATORS.BANK_ACCOUNT_NUMBER
        accountHolderName: str = VALIDATORS.NAME
        aadharCardNumber: Optional[str] = VALIDATORS.AADHAAR_CARD_NUMBER
        aadharName: Optional[str] = VALIDATORS.NAME
        aadharImageFront: Optional[str] = ''
        aadharImageBack: Optional[str] = ''
        profileImage: Optional[str] = ''
        panCardNumber: Optional[str] = VALIDATORS.PAN_CARD_NUMBER
        panCardName: Optional[str] = VALIDATORS.NAME
        panCardImage: Optional[str] = ''
    



class LoginRequest(BaseModel):
    username: str = VALIDATORS.USER_ID
    password: str = VALIDATORS.PASSWORD

    
class ResetPassword(BaseModel):
    request_id_enc: str = VALIDATORS.REQUIRED
    new_password: str = VALIDATORS.PASSWORD

    
class ContactVerificationOTP(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    contact_type: str = VALIDATORS.CONTACT_TYPE
    email_id_or_mobile_no: str = VALIDATORS.EMAIL_OR_MOBILE_NUMBER
    otp: str = VALIDATORS.OTP
    
    