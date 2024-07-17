
from fastapi import APIRouter, Depends
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, INVALID_USER_ID, OK
from src.misc.security.Jwt import get_current_user
from src.schemas.TeamDetails import DayWiseBusinessDetailsRequest, DirectDetailsRequest, DownlineDetailsRequest
from src.data_access.team import team as data_access
from src.misc.security.RightsChecker import RightsChecker
from src.utilities.utils import dataFrameToJsonObject, get_error_message


router = APIRouter(
    tags=["Team Details"]
)

@router.post('/direct_details', dependencies=[Depends(RightsChecker([30, 33])), Depends(get_current_user)])
def direct_details(req: DirectDetailsRequest, token_payload: any = Depends(get_current_user)):
    try:
        user_id_token = token_payload["user_id"]

        if(req.sponsor_id==user_id_token or token_payload["role"]=="Admin"):
            dataset = data_access.getDirectDetails(req)
            if len(dataset)>0:
                ds = dataset['rs']
                return { 'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }
                    
            return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }
        return {'success': False, 'message': INVALID_USER_ID }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/downline_details', dependencies=[Depends(RightsChecker([31, 34])), Depends(get_current_user)])
def downline_details(req: DownlineDetailsRequest, token_payload: any = Depends(get_current_user)):
    try:
        user_id_token = token_payload["user_id"]

        if(req.user_id==user_id_token or token_payload["role"]=="Admin"):
            dataset = data_access.getDownlineDetails(req)
            if len(dataset)>0:
                ds = dataset['rs']
                return { 'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }
                    
            return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }
        return {'success': False, 'message': INVALID_USER_ID }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/day_wise_business_details', dependencies=[Depends(RightsChecker([35, 36])), Depends(get_current_user)])
def day_wise_business_details(req: DayWiseBusinessDetailsRequest, token_payload: any = Depends(get_current_user)):
    try:
        user_id_token = token_payload["user_id"]

        if(req.user_id==user_id_token or token_payload["role"]=="Admin"):
            dataset = data_access.getDayWiseBusinessDetails(req)
            if len(dataset)>0:
                ds = dataset['rs']
                return { 'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }
                    
            return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }
        return {'success': False, 'message': INVALID_USER_ID }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
