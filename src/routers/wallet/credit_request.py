
import json
from fastapi import APIRouter, Depends
from src.misc.security.RightsChecker import RightsChecker
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.wallet import credit_request as data_access

from src.misc.security.Jwt import get_current_user
from src.schemas.Wallet import CreditRequestApproveRejectDataItem, GetCreditRequests, RequestForCredit
from src.utilities.aes import aes
from src.utilities.utils import dataFrameToJsonObject, get_error_message


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.post('/request_for_credit', dependencies=[Depends(RightsChecker([102, 103]))])
async def request_for_credit(req: RequestForCredit, token_payload:any = Depends(get_current_user)):
    try:

        user_id = token_payload["user_id"]
        user_type = token_payload["role"]

        payment_request_id = aes.decrypt(req.payment_request_id)
        
        dataset = data_access.request_for_credit(req=req, user_id=user_id, user_type=user_type, payment_request_id=payment_request_id)
        if len(dataset)>0:
            ds = dataset['rs']
            
            if (ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
    
    
@router.post('/get_credit_requests', dependencies=[Depends(RightsChecker([104, 105, 106]))])
async def get_credit_requests(req: GetCreditRequests, token_payload:any = Depends(get_current_user)):
    try:
        match_exact_user_id=False

        if(token_payload["role"]!='Admin'):
            req.user_id = token_payload["user_id"]
            req.user_type = token_payload["role"]
            match_exact_user_id = True

        dataset = data_access.get_credit_request(req=req, match_exact_user_id=match_exact_user_id)
        if len(dataset)>0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }
            
        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
    
    
@router.put('/update_credit_requests_status', dependencies=[Depends(RightsChecker([104]))])
async def update_credit_requests_status(dataItems:list[CreditRequestApproveRejectDataItem], token_payload:any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]
        user_type = token_payload["role"]
        
        data_dicts = json.dumps([item.dict() for item in dataItems])
        # print(data_dicts)
        dataset = data_access.update_credit_requests_status(by_user_id=user_id, by_user_type=user_type, data_dicts=data_dicts)
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
    
    