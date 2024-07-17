
import json
from typing import Union
from fastapi import APIRouter, Query
from src.misc.helpers.email_helper import send_contact_verification_otp_mail, send_email_verification_link_mail
from src.misc.helpers.sms_helper import send_contact_verification_otp_sms
from src.misc.helpers.helper_utils import get_route_by_control_id
from src.utilities.aes import aes
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR
from src.misc.decorators.accounts_decorators import is_valid_login_id
from src.schemas.Accounts import ContactVerificationOTP
from src.utilities.utils import get_error_message, company_details
from src.data_access.accounts import contact_verification as data_access
from src.misc.constants import VALIDATORS

router = APIRouter(
    tags=["Contact Verification"]
)

@router.get('/get_contact_verification_otp')
@is_valid_login_id
def get_contact_verification_otp(user_id: str = VALIDATORS.USER_ID, contact_type: str=VALIDATORS.CONTACT_TYPE, email_id_or_mobile_no: str=VALIDATORS.EMAIL_OR_MOBILE_NUMBER, login_id: str=VALIDATORS.LOGIN_ID):
    try:
        dataset = data_access.getOTPForContactVerification(user_id=user_id, contact_type=contact_type, email_id_or_mobile_no=email_id_or_mobile_no)
        
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']

            if(ds.iloc[0].loc['success']):
                otp = ds.iloc[0].loc['otp']

                if(contact_type=='Mobile'):
                    is_sms_sent, sent_message = send_contact_verification_otp_sms(user_id=user_id, user_name=ds.iloc[0].loc['user_name'], mobile_no=email_id_or_mobile_no, otp=otp)
                    return {'success': is_sms_sent, 'message': sent_message }


                if(contact_type=='Email'):
                    is_email_sent, sent_message = send_contact_verification_otp_mail(user_id=user_id, user_name=ds.iloc[0].loc['user_name'], email_id=email_id_or_mobile_no, otp=otp)
                    return {'success': is_email_sent, 'message': sent_message }

            return {'success': False, 'message': ds.iloc[0].loc['message'] }

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }


    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/submit_contact_verification_otp')
def submit_contact_verification_otp(request: ContactVerificationOTP):
    try:
        dataset = data_access.submitOTPForContactVerification(user_id=request.user_id, contact_type=request.contact_type, email_id_or_mobile_no=request.email_id_or_mobile_no, otp=request.otp)

        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            # print(ds.iloc[0].loc['success'])
            if(ds.iloc[0].loc['success']):
                return {'success': True, 'message': ds.iloc[0].loc['message'] }

            return {'success': False, 'message': ds.iloc[0].loc['message'] }

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }


    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_email_verification_link')
@is_valid_login_id
def get_email_verification_link(user_id: str = VALIDATORS.USER_ID, email_id: str = VALIDATORS.EMAIL_ID, login_id: str=VALIDATORS.LOGIN_ID):
    try:
        dataset = data_access.getOTPForContactVerification(user_id=user_id, contact_type='Email', email_id_or_mobile_no=email_id)

        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']

            if(ds.iloc[0].loc['success']):
                otp = ds.iloc[0].loc['otp']
                
                d = {'user_id': user_id, 'contact_type': 'Email', 'email_id_or_mobile_no': email_id, 'otp': otp}
                d_str = json.dumps(d, separators=(',',':'))
                d_str = aes.encrypt(d_str)

                path = get_route_by_control_id('email_verification_link')['url'][1:]

                verification_link = company_details['website']+path+'/'+d_str
                print(verification_link)

                is_email_sent, sent_message = send_email_verification_link_mail(user_id=user_id, user_name=ds.iloc[0].loc['user_name'], verification_link=verification_link, email_id=email_id)
            
                return {'success': is_email_sent, 'message': 'Verification link sent successfully!' if is_email_sent else sent_message }

            return {'success': False, 'message': ds.iloc[0].loc['message'] }

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/verify_email_from_link')
def verify_email_from_link(data: str):
    try:
        data = aes.decrypt(data)
        data = json.loads(data)
        
        dataset = data_access.submitOTPForContactVerification(user_id=data['user_id'], contact_type=data['contact_type'], email_id_or_mobile_no=data['email_id_or_mobile_no'], otp=data['otp'])

        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            # print(ds.iloc[0].loc['success'])
            if(ds.iloc[0].loc['success']):
                return {'success': True, 'message': 'Email verified successfully!' }

            return {'success': False, 'message': 'Invalid or expired verification link!' }

        return {'success': False, 'message': 'Invalid or expired verification link!' }


    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': 'Invalid verification link!'}
