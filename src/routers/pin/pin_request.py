
from datetime import datetime
import json
import os
from fastapi import APIRouter, Depends, File, UploadFile
from src.misc.security.RightsChecker import RightsChecker
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, OK, UNSUPPORTED_FILE_FORMAT
from src.data_access.pin import pin_request as data_access
from src.misc.security.Jwt import get_current_user
from src.schemas.Pin import GetPinRequest, PinRequest, PinRequestApproveRejectDataItem
from src.utilities.utils import dataFrameToJsonObject, get_error_message
from src.misc.constants import VALIDATORS
from src.utilities.aes import aes


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.post('/request_for_pins', dependencies=[Depends(RightsChecker([56, 68]))])
async def request_for_pins(req: PinRequest, token_payload:any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]
        user_type = token_payload["role"]
        
        payment_request_id = aes.decrypt(req.payment_request_id)
        
        dataset = data_access.request_for_pins(user_id=user_id, user_type=user_type, payment_request_id=payment_request_id, pins=json.dumps(req.pins))
        if len(dataset)>0 and len(dataset['rs'])>0:
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"] }
            
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
        
        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
    
    
@router.post('/get_pin_requests', dependencies=[Depends(RightsChecker([57, 58, 69]))])
async def get_pin_requests(req: GetPinRequest, token_payload:any = Depends(get_current_user)):
    try:
        match_exact_user_id=False
        user_type = token_payload["role"]

        if(user_type!='Admin'):
            match_exact_user_id = True

        dataset = data_access.get_pin_request(req=req, match_exact_user_id=match_exact_user_id)
        if len(dataset)>0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }
            
        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
    

@router.get('/get_pin_requests_details', dependencies=[Depends(RightsChecker([57, 58, 69]))])
async def get_pin_requests_details(req_id: int):
    try:
        dataset = data_access.get_pin_request_details(req_id=req_id)
        if len(dataset)>0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds) }
            
        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
    
    
@router.put('/update_pin_requests_status', dependencies=[Depends(RightsChecker([57]))])
async def update_pin_requests_status(dataItems:list[PinRequestApproveRejectDataItem], token_payload:any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]
        user_type = token_payload["role"]
        
        data_dicts = json.dumps([item.dict() for item in dataItems])
        print(data_dicts)
        dataset = data_access.update_pin_requests_status(by_user_id=user_id, by_user_type=user_type, data_dicts=data_dicts)
        if len(dataset)>0:
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                return {
                        'success': True, 
                        'message': ds.iloc[0].loc["message"], 
                        'approved_count': int(ds.iloc[0].loc["approved_count"]),
                        'rejected_count': int(ds.iloc[0].loc["rejected_count"])
                        }
            
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
        
        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
    
    