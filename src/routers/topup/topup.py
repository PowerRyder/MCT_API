
from fastapi import APIRouter, Depends
from src.data_access.topup import topup as data_access
from src.misc.constants.messages import (DATABASE_CONNECTION_ERROR, OK)
from src.misc.helpers.topup_helper import send_topup_mail_and_sms
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.Topup import (RoiBlockUnblockRequest, TopupByPinRequest, TopupDetailsRequest,
                               TopupFromWalletRequest)
from src.utilities.aes import aes
from src.utilities.utils import dataFrameToJsonObject, get_error_message, company_details



router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post('/topup_by_pin', dependencies=[Depends(RightsChecker([76, 77, 78]))])
def topup_by_pin(req: TopupByPinRequest, token_payload: any = Depends(get_current_user)):
    try:
        if(req.two_factor_auth_request_id!=''):
            req.two_factor_auth_request_id = int(aes.decrypt(req.two_factor_auth_request_id))
        else:
            req.two_factor_auth_request_id = 0
            
        dataset = data_access.topup_by_pin(req=req, by_user_id=token_payload["user_id"],
                                            by_user_type=token_payload["role"])
        # print(dataset)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if (ds.iloc[0].loc["success"]):
                send_topup_mail_and_sms(ds)
                # send_topup_sms(ds.iloc[0].loc["user_id"], ds.iloc[0].loc["user_name"], ds.iloc[0].loc["mobile_no"], ds.iloc[0].loc["package_name"])
                
                # send_topup_mail(ds.iloc[0].loc["user_id"], ds.iloc[0].loc["user_name"], ds.iloc[0].loc["email_id"], ds.iloc[0].loc["package_name"], amount )
                
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/topup_from_wallet', dependencies=[Depends(RightsChecker([79, 80, 81]))])
def topup_from_wallet(req: TopupFromWalletRequest, token_payload: any = Depends(get_current_user)):
    try:
        if(req.two_factor_auth_request_id!=''):
            req.two_factor_auth_request_id = int(aes.decrypt(req.two_factor_auth_request_id))
        else:
            req.two_factor_auth_request_id = 0
            
        dataset = data_access.topup_from_wallet(req=req, by_user_id=token_payload["user_id"],
                                            by_user_type=token_payload["role"])
        # print(dataset)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if (ds.iloc[0].loc["success"]):
                send_topup_mail_and_sms(ds)
                
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/topup_details', dependencies=[Depends(RightsChecker([82, 83, 84]))])
def topup_details(req: TopupDetailsRequest, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        match_exact_by_user_id = False
        if(token_payload["role"]=='User'):
            if(req.topup_for=='User'):
                req.user_id = token_payload["user_id"]
                req.by_user_id = ''
                req.by_user_type = 'All'
                match_exact_user_id = True
                
            elif(req.topup_for=='Other'):
                req.user_id = ''
                req.by_user_id = token_payload["user_id"]
                req.by_user_type = token_payload["role"]
                match_exact_by_user_id = True
                
            else: # Downline
                req.user_id = token_payload["user_id"]
        
        elif(token_payload["role"]=='Franchise'):
            req.topup_for = 'User' # Franchise cannot see downline topup
            req.by_user_id = token_payload["user_id"]
            req.by_user_type = token_payload["role"]
            match_exact_by_user_id = True
        
        if(not (company_details['is_binary_system'])):
            req.side = 'All'
        
        dataset = data_access.topup_details(req=req, match_exact_user_id=match_exact_user_id, match_exact_by_user_id=match_exact_by_user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }
            
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.put('/toggle_roi_block_status', dependencies=[Depends(RightsChecker([82]))])
def toggle_roi_block_status(req: RoiBlockUnblockRequest, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.toggle_roi_block_status(req=req, by_admin_user_id=token_payload["user_id"])
        # print(dataset)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if (ds.iloc[0].loc["success"]):
                
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.delete('/delete_topup', dependencies=[Depends(RightsChecker([82]))])
def delete_topup(pin_srno: int, remarks: str='', token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.delete_topup(pin_srno=pin_srno, remarks=remarks, by_admin_user_id=token_payload["user_id"])
        # print(dataset)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if (ds.iloc[0].loc["success"]):
                
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
