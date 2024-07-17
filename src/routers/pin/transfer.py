
from fastapi import APIRouter, Depends
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.pin import transfer as data_access
from src.schemas.Pin import PinTransferHistoryRequest, PinTransferRequest
from src.utilities.utils import dataFrameToJsonObject, get_error_message
from src.utilities.aes import aes


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get('/get_available_pin_count_for_transfer', dependencies=[Depends(RightsChecker([52, 53, 66]))])
def get_available_pin_count_for_transfer(userId: str, packageId: int):
    try:
        dataset = data_access.get_available_pin_count_for_transfer(userId=userId, packageId=packageId)
        
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']

            if(ds.iloc[0].loc["success"]):
                return {'success': True, 'message': OK, 'no_of_pins_available': int(ds.iloc[0].loc["no_of_pins_available"]) }
            
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
        
        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success' : False, 'message' : get_error_message(e)}
    

@router.post('/transfer_pins', dependencies=[Depends(RightsChecker([52, 53, 66]))])
def transfer_pins(req: PinTransferRequest, token_payload: any = Depends(get_current_user)):
    try:

        by_user_id=token_payload["user_id"]

        if(req.two_factor_auth_request_id!=''):
            req.two_factor_auth_request_id = int(aes.decrypt(req.two_factor_auth_request_id))
        else:
            req.two_factor_auth_request_id = 0
            
        dataset = data_access.transfer_pins(req=req, by_user_id=by_user_id)
        
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']

            if(ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"] }
            
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
        
        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success' : False, 'message' : get_error_message(e)}
    

@router.post('/get_pin_transfer_history', dependencies=[Depends(RightsChecker([54, 55, 67]))])
def get_pin_transfer_history(req: PinTransferHistoryRequest, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_from_user_id = False
        match_exact_to_user_id = False

        if(token_payload["role"]!="Admin"):
            if(req.type=="From"):
                req.from_user_id = token_payload["user_id"]
                req.from_user_type = token_payload["role"]
                match_exact_from_user_id = True

            if(req.type=="To"):
                req.to_user_id = token_payload["user_id"]
                req.to_user_type = token_payload["role"]
                match_exact_to_user_id = True
            

        dataset = data_access.get_pin_transfer_history(req, match_exact_from_user_id, match_exact_to_user_id)
        if len(dataset)>0:
            ds = dataset['rs']
            return { 'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }
                
        return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
    