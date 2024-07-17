
from fastapi import APIRouter, Depends
from src.misc.constants.messages import INVALID_USER_ID, OK
from src.data_access.franchise import details as data_access
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.utilities.utils import dataFrameToJsonObject, get_error_message
from src.misc.constants import VALIDATORS


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get('/details', dependencies=[Depends(RightsChecker([59, 93, 97, 98, 183]))])
def details(user_id: str = VALIDATORS.USER_ID, token_payload: any = Depends(get_current_user)):
    try:
        user_id_token = token_payload["user_id"]
        # print("here")
        # if(user_id==user_id_token or token_payload["role"]=='Admin'):
        dataset = data_access.get_franchise_details(user_id=user_id)
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["valid"]):
                return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds) }
            
        return {'success': False, 'message': INVALID_USER_ID }
        # return {'success': False, 'message': INVALID_USER_ID }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/dashboard_details', dependencies=[Depends(RightsChecker([60]))])
def dashboard_details(token_payload: any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]

        dataset = data_access.get_franchise_dashboard_details(user_id=user_id)
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["valid"]):
                return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'wallet_balances': dataFrameToJsonObject(dataset['rs_wallet_balance'])}
            
            return {'success': False, 'message': INVALID_USER_ID }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

