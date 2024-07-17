
import json
from fastapi import APIRouter
import requests
from src.misc.helpers.email_helper import send_joining_mail
from src.misc.helpers.sms_helper import send_joining_sms
from src.routers.docs.welcome_letter import get_welcome_letter_pdf_bytes
from src.utilities.aes import aes
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, INVALID_USER_ID, JOINING_INFO_ALREADY_SENT, JOINING_INFO_SEND_ERROR, OK
from src.schemas.Accounts import Register
from src.utilities.utils import addCurrencySymbol, dataFrameToJsonObject, get_error_message, company_details
from src.data_access.user import details as user_details_data_access
from src.data_access import misc as misc_data_access
from src.data_access.accounts import register as register_data_access
from src.utilities.utils import config, company_details, get_error_message, hide_email_address, hide_mobile_no
from src.misc.constants import VALIDATORS


router = APIRouter(
    tags=["Register"]
)

@router.post('/register')
def register(request: Register):
    try:
        # start_time = time.time()
        d = json.dumps([])
        if company_details['is_crypto_system']:
            supported_crypto = misc_data_access.get_supported_cryptos(unique_chains_only=True)['rs']
            chains = ",".join(supported_crypto.loc[:, 'chain'].values)
            response = requests.get("https://hiicall.com/Blockchain/crypto/api/Accounts/CreateAccount?chains=%s&appKey=%s" % (chains, config['CryptoAppKey']))
            result = json.loads(response.text)
            
            d = json.dumps([{'Chain': k, 'Address': v} for k,v in result['data'].items()])
        dataset = register_data_access.register(request, d)
        # print(dataset)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                
                send_joining_mail_and_sms(aes.encrypt(ds.iloc[0].loc["user_id"]))
                # end_time = time.time()
                # print("--- %s seconds ---" % (end_time - start_time))
                return {'success': True, 'message': ds.iloc[0].loc["message"], 'user_id': ds.iloc[0].loc["user_id"] }
        
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

@router.get('/is_sponsor_valid')
def is_sponsor_valid(sponsor_id: str = VALIDATORS.USER_ID):
    try:
        dataset = register_data_access.isSponsorValid(sponsor_id=sponsor_id)
        # print(dataset)
        
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            ds = dataFrameToJsonObject(ds)
            return {'success': True, 'message': OK, 'data': ds }
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/is_upline_valid')
def is_upline_valid(upline_user_id: str = VALIDATORS.USER_ID):
    try:
        dataset = register_data_access.isUplineValid(upline_user_id=upline_user_id)
        # print(dataset)
        
        if(len(dataset)>0 and len(dataset['rs'])):
            ds = dataset['rs']
            ds = dataFrameToJsonObject(ds)
            return {'success': True, 'message': OK, 'data': ds }
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

@router.get('/does_user_id_exist')
def does_user_id_exist(user_id: str = VALIDATORS.USER_ID):
    try:
        dataset = register_data_access.doesUserIdExist(user_id=user_id)
        # print(dataset)
        
        if(len(dataset)>0 and len(dataset['rs'])):
            ds = dataset['rs']
            ds = dataFrameToJsonObject(ds)
            return {'success': True, 'message': OK, 'data': ds }
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/send_joining_mail_and_sms')
def send_joining_mail_and_sms(id_enc: str):
    try:
        user_id = aes.decrypt(id_enc)

        dataset = user_details_data_access.get_user_details(user_id=user_id)
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["valid"]):
                is_email_sent=False
                is_sms_sent=False

                if(ds.iloc[0].loc["is_joining_mail_sent"] and ds.iloc[0].loc["is_joining_sms_sent"]):
                    return {'success': False, 'message': JOINING_INFO_ALREADY_SENT }

                email_id = ds.iloc[0].loc['email_id']
                if(not ds.iloc[0].loc["is_joining_mail_sent"]):
                    pdf_bytes = get_welcome_letter_pdf_bytes(ds.iloc[0].loc["user_id"])
                    is_email_sent, sent_message = send_joining_mail(user_id=ds.iloc[0].loc['user_id'],
                                                                    user_name=ds.iloc[0].loc['name'],
                                                                    email_id=email_id,
                                                                    joining_amount=addCurrencySymbol(str(round(ds.iloc[0].loc['joining_amount'], int(company_details['round_off_digits'])))),
                                                                    sponsor_id=ds.iloc[0].loc['sponsor_id'],
                                                                    referral_link=ds.iloc[0].loc['referral_link'], 
                                                                    in_memory_files=[('Welcome_Letter.pdf', pdf_bytes)])

                mobile_no = ds.iloc[0].loc['mobile_no']
                if(not ds.iloc[0].loc["is_joining_sms_sent"]):
                    is_sms_sent, sent_message = send_joining_sms(user_id=ds.iloc[0].loc['user_id'], user_name=ds.iloc[0].loc['name'], mobile_no=mobile_no)
                
                register_data_access.updateJoiningMailAndSmsStatus(user_id=user_id, is_email_sent=is_email_sent, is_sms_sent=is_sms_sent)

                if(is_email_sent or is_sms_sent):
                    msg = "Your joining info is sent to your" + ((" mobile number" + hide_mobile_no(mobile_no=mobile_no)) if(is_sms_sent) else "") + (" and " if(is_sms_sent and is_email_sent) else "") + (" email id "+ hide_email_address(email_id=email_id) if(is_sms_sent) else "") +"."
                    return {'success': True, 'message': msg }

                return {'success': False, 'message': JOINING_INFO_SEND_ERROR }

            return {'success': False, 'message': INVALID_USER_ID }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
