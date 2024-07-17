
from fastapi import APIRouter, Depends
from src.misc.security.RightsChecker import RightsChecker
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.wallet import fund_transfer as data_access

from src.misc.security.Jwt import get_current_user
from src.schemas.Wallet import TransferFundHistoryRequest, WalletTransferFund
from src.utilities.utils import dataFrameToJsonObject, get_error_message
from src.utilities.aes import aes


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.post('/transfer_fund', dependencies=[Depends(RightsChecker([96, 97, 98]))])
async def transfer_fund(req: WalletTransferFund, token_payload:any = Depends(get_current_user)):
    try:

        by_user_id = token_payload["user_id"]
        by_user_type = token_payload["role"]

        if(req.two_factor_auth_request_id!=''):
            req.two_factor_auth_request_id = int(aes.decrypt(req.two_factor_auth_request_id))
        else:
            req.two_factor_auth_request_id = 0
            
        if(token_payload["role"]!="Admin"):
            req.from_user_id = token_payload["user_id"]
            req.from_user_type = token_payload["role"]
            
        dataset = data_access.transfer_fund(req=req, by_user_id=by_user_id, by_user_type=by_user_type)
        if len(dataset)>0:
            ds = dataset['rs']
            
            if (ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
    

@router.post('/fund_transfer_history', dependencies=[Depends(RightsChecker([96, 97, 98]))])
async def fund_transfer_history(req: TransferFundHistoryRequest, token_payload:any = Depends(get_current_user)):
    try:
        match_exact_from_user_id = False
        match_exact_to_user_id = False
        print(req)
        if(token_payload["role"]!="Admin"):
            if(req.is_from):
                req.from_user_id = token_payload["user_id"]
                req.from_user_type = token_payload["role"]
                match_exact_from_user_id = True
            else:
                req.to_user_id = token_payload["user_id"]
                req.to_user_type = token_payload["role"]
                match_exact_to_user_id = True
                
            
        dataset = data_access.fund_transfer_history(req=req, match_exact_from_user_id=match_exact_from_user_id, match_exact_to_user_id=match_exact_to_user_id)
        
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }
            
        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
    
