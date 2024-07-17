
from fastapi import APIRouter, Depends
from src.schemas.Pin import PinStatisticsRequest, ViewPinRequest
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, INVALID_USER_ID, OK
from src.data_access.pin import pin as data_access
from src.utilities.utils import dataFrameToJsonObject, get_error_message


router = APIRouter()

@router.get('/getPinDetails')
def get_pin_details(pin_number: int, pin_password: int):
    try:
        dataset = data_access.get_pin_details(pinNumber=pin_number, pinPassword=pin_password)
        # print(dataset)
        if len(dataset)>0 :
            dataset = dataset['rs']

            if len(dataset) > 0:
                ds = dataFrameToJsonObject(dataset)
                return {'success': True, 'message': OK, 'data': ds }
            
        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success' : False, 'message' : get_error_message(e)}
    

@router.post('/view_pins', dependencies=[Depends(RightsChecker([44, 45, 62]))])
def view_pins(req: ViewPinRequest, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if(token_payload["role"]!="Admin"):
            req.user_id = token_payload["user_id"]
            req.user_type = token_payload["role"]
            match_exact_user_id = True

        dataset = data_access.view_pins(req, match_exact_user_id)
        if len(dataset)>0:
            ds = dataset['rs']
            return { 
                    'success': True,
                    'message': OK,
                    'data': dataFrameToJsonObject(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]),
                    'transferred_pins_count': int(dataset['rs2'].iloc[0].loc["transferred_pins_count"])
                    }
                
        return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
    

@router.post('/pin_statistics', dependencies=[Depends(RightsChecker([50, 51, 65]))])
def pin_statistics(req: PinStatisticsRequest, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if(token_payload["role"]!="Admin"):
            req.user_id = token_payload["user_id"]
            req.user_type = token_payload["role"]
            match_exact_user_id = True

        dataset = data_access.pin_statistics(req, match_exact_user_id)
        if len(dataset)>0:
            ds = dataset['rs']
            return { 'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }
                
        return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
    