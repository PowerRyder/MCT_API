
from fastapi import APIRouter
from src.misc.helpers.helper_utils import get_route_by_control_id
from src.misc.helpers.email_helper import send_reset_password_link_mail
from src.misc.helpers.sms_helper import send_reset_password_link_sms
from src.utilities.aes import aes
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.schemas.Accounts import ResetPassword
from src.utilities.utils import dataFrameToJsonObject, get_error_message, hide_email_address, hide_mobile_no, company_details
from src.data_access.accounts import forgot_password as data_access
from src.utilities.utils import company_details
from src.misc.constants import VALIDATORS

router = APIRouter(
    tags=["Forgot Password"]
)


@router.get('/get_password_reset_link')
def get_password_reset_link(user_id:str = VALIDATORS.USER_ID):
    try:
        is_email_sent = False
        is_sms_sent = False

        req_ds = data_access.requestForResetPassword(user_id=user_id)
        
        if len(req_ds)>0 and len(req_ds['rs']):
            req_ds = req_ds['rs']
            if(req_ds.iloc[0].loc["success"]):
                path = get_route_by_control_id('forgot_password')['url'][1:]

                reset_link = company_details['website']+path+'/'+aes.encrypt(str(req_ds.iloc[0].loc["request_id"]))
                print(reset_link)

                email_id = req_ds.iloc[0].loc['email_id'] 
                is_email_sent, sent_message = send_reset_password_link_mail(user_id=req_ds.iloc[0].loc['user_id'], user_name=req_ds.iloc[0].loc['name'], email_id=email_id, reset_link=reset_link)
            
                mobile_no = req_ds.iloc[0].loc['mobile_no']
                is_sms_sent, sent_message = send_reset_password_link_sms(user_id=req_ds.iloc[0].loc['user_id'], user_name=req_ds.iloc[0].loc['name'], mobile_no=mobile_no, reset_link=reset_link)
                
                if(is_email_sent or is_sms_sent):
                    msg = "A reset link is sent to your" + ((" mobile number " + hide_mobile_no(mobile_no=mobile_no)) if(is_sms_sent) else "") + (" and " if(is_sms_sent and is_email_sent) else "") + (" email id "+ hide_email_address(email_id=email_id) if(is_email_sent) else "") +"."
                    return {'success': True, 'message': msg }

                return {'success': False, 'message': "Some error occurred while sending the reset link. Please contact your administrator for further support!" }

            return {'success': False, 'message': req_ds.iloc[0].loc["message"] }
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

@router.get('/check_reset_password_request_validity')
def check_reset_password_request_validity(request_id_enc: str):
    try:
        request_id = aes.decrypt(request_id_enc)
        request_id = int(request_id)
        dataset = data_access.checkRequestForResetPasswordValidity(request_id=request_id)

        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']

            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds) }

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }


    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/reset_password')
def reset_password(request: ResetPassword):
    try:
        request_id = aes.decrypt(request.request_id_enc)
        request_id = int(request_id)
        dataset = data_access.resetPassword(request_id=request_id, new_password=request.new_password)

        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']

            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds) }

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }


    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
