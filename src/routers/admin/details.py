
from fastapi import APIRouter, Depends
from src.misc.constants.messages import INVALID_USER_ID, OK, DATABASE_CONNECTION_ERROR
from src.data_access.admin import details as data_access
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.utilities.utils import dataFrameToJsonObject, get_error_message
from src.misc.constants import VALIDATORS


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get('/details', dependencies=[Depends(RightsChecker([11]))])
def details(admin_user_id: str = VALIDATORS.USER_ID, token_payload: any = Depends(get_current_user)):
    try:
        user_id_token = token_payload["user_id"]

        if(admin_user_id==user_id_token):
            dataset = data_access.get_admin_details(admin_user_id=admin_user_id)
            if len(dataset)>0 and len(dataset['rs']):
                ds = dataset['rs']
                if(ds.iloc[0].loc["valid"]):
                    return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds) }
                
            return {'success': False, 'message': INVALID_USER_ID }
        return {'success': False, 'message': INVALID_USER_ID }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/dashboard_details', dependencies=[Depends(RightsChecker([15]))])
def dashboard_details(token_payload: any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]

        dataset = data_access.get_admin_dashboard_details(admin_user_id=user_id)
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["valid"]):
                return {
                    'success': True,
                    'message': OK,
                    'data': dataFrameToJsonObject(ds),
                    'income_distribution': dataFrameToJsonObject(dataset['rs_income_distribution']),
                    'packages_sales': dataFrameToJsonObject(dataset['rs_packages_sales']),
                    'top_earners': dataFrameToJsonObject(dataset['rs_top_earners'])
                }
            
            return {'success': False, 'message': INVALID_USER_ID }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}



@router.get('/dashboard_chart_details', dependencies=[Depends(RightsChecker([15]))])
def dashboard_chart_details(duration: str = VALIDATORS.CHART_DURATION, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_admin_dashboard_chart_details(duration=duration)

        if len(dataset):
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(dataset['rs'])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
