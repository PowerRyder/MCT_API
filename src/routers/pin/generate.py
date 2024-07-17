
from fastapi import APIRouter, Depends
from src.misc.security.RightsChecker import RightsChecker
from src.misc.security.Jwt import get_current_user
from src.misc.constants.messages import OK, DATABASE_CONNECTION_ERROR
from src.schemas.Pin import PinGenerateRequest
from src.data_access.pin import generate as data_access
from src.utilities.utils import dataFrameToJsonObject, get_error_message
from src.utilities.aes import aes


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.post('/generate_pins', dependencies=[Depends(RightsChecker([46, 47, 63]))])
def generate_pins(req: PinGenerateRequest, token_payload: any = Depends(get_current_user)):
    try:
        if(req.two_factor_auth_request_id!=''):
            req.two_factor_auth_request_id = int(aes.decrypt(req.two_factor_auth_request_id))
        else:
            req.two_factor_auth_request_id = 0
            
        dataset = data_access.generate_pins(req=req, by_user_id=token_payload["user_id"], by_user_type=token_payload["role"])
        # print(dataset)
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"] }
            
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
        
        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}
    
    except Exception as e:
        print(e.__str__())
        return {'success' : False, 'message' : get_error_message(e)}
    

@router.get('/get_pin_generate_history', dependencies=[Depends(RightsChecker([46, 47, 63]))])
def get_pin_generate_history(page_index: int, page_size: int, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_pin_generate_history(by_user_id=token_payload["user_id"], by_user_type=token_payload["role"], page_index=page_index, page_size=page_size)
        # print(dataset)
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }
            
        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}
    
    except Exception as e:
        print(e.__str__())
        return {'success' : False, 'message' : get_error_message(e)}
    