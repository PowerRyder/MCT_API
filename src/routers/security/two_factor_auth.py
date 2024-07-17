
import pyotp
from src.misc.security.Jwt import get_current_user
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, INVALID_OTP_OPTION, INVALID_USER_ID, INVALID_VERIFICATION_CODE, INVALID_VERIFICATION_MODE, NO_EMAIL_FOR_MAIL, NO_MOBILE_FOR_SMS, OK, OTP_SENT_SUCCESSFULLY_TO_EMAIL, OTP_SENT_SUCCESSFULLY_TO_MOBILE
from src.misc.helpers.email_helper import send_two_factor_auth_otp_mail
from src.misc.helpers.sms_helper import send_two_factor_auth_otp_sms
from src.data_access.security import two_factor_auth as data_access
from fastapi import APIRouter, Depends
from src.utilities.aes import aes
from src.schemas.Security import TwoFactorAuthenticationRequest
from src.utilities.utils import company_details, generate_google_authenticator_secret_key, get_error_message, hide_email_address, hide_mobile_no, is_valid_google_authenticator_code
from src.misc.constants import VALIDATORS
import pyqrcode


router = APIRouter(
    tags=["Two Factor Auth"]
)

@router.get('/toggle_two_factor_auth', dependencies=[Depends(get_current_user)])
def toggle_two_factor_auth(two_factor_auth_request_id: str='', token_payload:any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]
        user_type = token_payload["role"]

        if(two_factor_auth_request_id!=''):
            two_factor_auth_request_id = int(aes.decrypt(two_factor_auth_request_id))
        else:
            two_factor_auth_request_id = 0
            
        dataset = data_access.toggle_two_factor_auth(user_id=user_id, user_type=user_type, two_factor_auth_request_id=two_factor_auth_request_id)
        
        if(len(dataset)>0 and len(dataset['rs'])):
            ds = dataset['rs']

            if(bool(ds.iloc[0].loc['success'])):
                return {'success':True, 'message': ds.iloc[0].loc['message'], 'two_factor_enabled': bool(ds.iloc[0].loc['two_factor_enabled'])}
            
            return {'success':False, 'message': ds.iloc[0].loc['message']}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/toggle_google_authenticator', dependencies=[Depends(get_current_user)])
def toggle_google_authenticator(token_payload:any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]
        user_type = token_payload["role"]

        dataset = data_access.toggle_google_authenticator(user_id=user_id, user_type=user_type)
        print(user_id, user_type)
        print(dataset)
        if(len(dataset)>0 and len(dataset['rs'])):
            ds = dataset['rs']

            if(bool(ds.iloc[0].loc['success'])):
                return {'success':True, 'message': ds.iloc[0].loc['message'], 'is_google_authenticator_enabled': bool(ds.iloc[0].loc['is_google_authenticator_enabled'])}
            
            return {'success':False, 'message': ds.iloc[0].loc['message']}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/setup_google_authenticator', dependencies=[Depends(get_current_user)])
def setup_google_authenticator(token_payload:any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]
        user_type = token_payload["role"]

        secret_key = generate_google_authenticator_secret_key()
        uri = pyotp.totp.TOTP(secret_key).provisioning_uri(name=user_id, issuer_name=company_details.loc["name"])
        qr = pyqrcode.create(uri)
        # print(uri)
        dataset = data_access.setup_google_authenticator(user_id=user_id, user_type=user_type, secret_key=secret_key)
        
        if(len(dataset)>0 and len(dataset['rs'])):
            ds = dataset['rs']

            if(bool(ds.iloc[0].loc['success'])):
                return {'success':True, 'message': ds.iloc[0].loc['message'], 'qr': "data:image/png;base64,"+qr.png_as_base64_str(scale=5)}
            
            return {'success':False, 'message': ds.iloc[0].loc['message']}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}



@router.get('/request_two_factor_auth', dependencies=[Depends(get_current_user)]) # User must be logged in
def request_two_factor_auth(user_id: str=VALIDATORS.USER_ID, user_type: str = VALIDATORS.USER_TYPE, purpose: str=VALIDATORS.TWO_FACTOR_AUTH_PURPOSE):
    try:
        dataset = data_access.request_two_factor_auth(user_id=user_id, user_type=user_type, purpose=purpose)
        
        if(len(dataset)>0 and len(dataset['rs'])):
            ds = dataset['rs']


            if(bool(ds.iloc[0].loc['success'])):
                request_id = ds.iloc[0].loc['request_id']
                request_id = aes.encrypt(str(request_id))
                return {'success': True, 'message': 'Ok', 'data': {
                    'request_id': request_id
                }}

            return {'success': False, 'message': ds.iloc[0].loc['message']}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

@router.get('/get_auth_modes_for_2fa_setup', dependencies=[Depends(get_current_user)])
def get_auth_modes_for_2fa_setup(user_id: str=VALIDATORS.USER_ID, token_payload:any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]
        user_type = token_payload["role"]

        # if(user_type=='Admin'):
        #     dataset = admin_data_access.get_admin_details(admin_user_id=user_id)
        # elif(user_type=='User'):
        #     dataset = user_data_access.get_user_details(user_id=user_id)

        dataset = data_access.get_auth_modes_for_setup(user_id=user_id, user_type=user_type)
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["valid"]):
                is_two_factor_enabled = bool(ds.iloc[0].loc['two_factor_enabled'])
                mobile_no = ds.iloc[0].loc['mobile_no']
                email_id = ds.iloc[0].loc['email_id']

                is_google_authenticator_enabled = bool(ds.iloc[0].loc['is_google_authenticator_enabled'])
                is_google_authenticator_setup = ds.iloc[0].loc['google_authenticator_key']!=""

                return {
                    'success': True,
                    'message': OK,
                    'data': {
                        'is_two_factor_enabled': is_two_factor_enabled,
                        'mobile_no': mobile_no,
                        'email_id': email_id,
                        'is_google_authenticator_enabled': is_google_authenticator_enabled,
                        'is_google_authenticator_setup': is_google_authenticator_setup
                    }}
            
            return {'success': False, 'message': INVALID_USER_ID }
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_auth_modes')
def get_auth_modes(user_id: str=VALIDATORS.USER_ID, request_id: str=VALIDATORS.REQUIRED):
    try:
        request_id = aes.decrypt(request_id)
        dataset = data_access.get_auth_modes(user_id=user_id, request_id=request_id)
        # print(dataset)
        if(len(dataset)>0 and len(dataset['rs'])):
            ds = dataset['rs']

            if(bool(ds.iloc[0].loc['success'])):
                mobile_no = ds.iloc[0].loc['mobile_no']
                email_id = ds.iloc[0].loc['email_id']

                is_google_authenticator_enabled = bool(ds.iloc[0].loc['is_google_authenticator_enabled'])
                google_authenticator_key = ds.iloc[0].loc['google_authenticator_key']
                # print(email_id)
                sign_in_options = []

                if(is_google_authenticator_enabled and google_authenticator_key != ''):
                    sign_in_options.append({"type": "Google_authenticator", "text": "Use Google Authenticator App"})

                if(email_id is not None and email_id != '' and company_details['is_email_configured']):
                    sign_in_options.append({"type": "Email", "text": "Send OTP to email "+hide_email_address(email_id)})

                if(mobile_no is not None and company_details['is_sms_configured']):
                    sign_in_options.append({"type": "Mobile", "text": "Send OTP to mobile "+hide_mobile_no(mobile_no)})

                return {'success': True, 'message': 'Ok', 'data': sign_in_options}

            return {'success': False, 'message': ds.iloc[0].loc['message']}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_auth_otp')
def get_auth_otp(user_id: str = VALIDATORS.USER_ID, request_id: str=VALIDATORS.REQUIRED, option: str=VALIDATORS.CONTACT_TYPE):
    try:
        request_id = aes.decrypt(request_id)
        dataset = data_access.get_auth_modes(user_id=user_id, request_id=request_id)
        # print(dataset)
        if(len(dataset)>0 and len(dataset['rs'])):
            ds = dataset['rs']

            if(bool(ds.iloc[0].loc['success'])):
                mobile_no = ds.iloc[0].loc['mobile_no']
                email_id = ds.iloc[0].loc['email_id']

                if(option=='Mobile'):
                    mobile_no = ds.iloc[0].loc['mobile_no']
                    
                    if(mobile_no != ''):
                        is_sent, sent_message = send_two_factor_auth_otp_sms(user_id=ds.iloc[0].loc['user_id'], user_name=ds.iloc[0].loc['name'], mobile_no=mobile_no, otp=ds.iloc[0].loc['otp'])
                        return {'success': is_sent, 'message': OTP_SENT_SUCCESSFULLY_TO_MOBILE.format(hide_mobile_no(mobile_no=mobile_no)) if is_sent else sent_message}
                    
                    return {'success': False, 'message': NO_MOBILE_FOR_SMS}
                
                elif(option=='Email'):
                    email_id = ds.iloc[0].loc['email_id']
                    if(email_id != ''):
                        is_sent, sent_message = send_two_factor_auth_otp_mail(user_id=user_id, user_name=ds.iloc[0].loc['name'], email_id=email_id, otp=ds.iloc[0].loc['otp'])
                        return {'success': is_sent, 'message': OTP_SENT_SUCCESSFULLY_TO_EMAIL.format(hide_email_address(email_id=email_id)) if is_sent else sent_message}
                    
                    return {'success': False, 'message': NO_EMAIL_FOR_MAIL}
                return {'success': False, 'message': INVALID_OTP_OPTION}
            return {'success': False, 'message': ds.iloc[0].loc['message']}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/submit_auth_code')
def submit_auth_code(auth_request: TwoFactorAuthenticationRequest):
    try:
        if(auth_request.mode not in ('Google_authenticator', 'Mobile', 'Email')):
            return {'success': False, 'message': INVALID_VERIFICATION_MODE}
        else:
            request_id = aes.decrypt(auth_request.request_id)
            is_valid_gauth_code = False
            if(auth_request.mode=="Google_authenticator"):
                dataset = data_access.get_auth_modes(user_id=auth_request.user_id, request_id=request_id)
                # print(dataset)
                
                if(len(dataset)>0 and len(dataset['rs'])):
                    ds = dataset['rs']
                    
                    if(bool(ds.iloc[0].loc['success'])):
                        google_authenticator_key = ds.iloc[0].loc['google_authenticator_key']
                        # print(google_authenticator_key)
                        
                        is_valid_gauth_code = is_valid_google_authenticator_code(google_authenticator_key, auth_request.code)

                        if(not is_valid_gauth_code):
                            return {'success': False, 'message': INVALID_VERIFICATION_CODE}
                        

            if(auth_request.mode in ('Mobile', 'Email') or is_valid_gauth_code):
                dataset = data_access.submit_two_factor_auth_code(request_id=request_id, mode=auth_request.mode, code=auth_request.code)
                # print(dataset)
                
                if(len(dataset)>0 and len(dataset['rs'])):
                    ds = dataset['rs']
                    
                    return {'success': bool(ds.iloc[0].loc['success']), 'message': ds.iloc[0].loc['message']}
            
                return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

            return {'success': False, 'message': INVALID_VERIFICATION_CODE}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
