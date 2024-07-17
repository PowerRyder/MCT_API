
from fastapi import APIRouter, Depends
from src.data_access.income import roi as data_access
from src.misc.constants.messages import (DATABASE_CONNECTION_ERROR, OK)
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.Income import GetROILevelIncome_Request, GetRoiIncome_Request, UpdateROIPercentage_Request
from src.utilities.utils import dataFrameToJsonObject, get_error_message


router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post('/get_roi_income', dependencies=[Depends(RightsChecker([140, 141]))])
def get_roi_income(req: GetRoiIncome_Request, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if(token_payload["role"]=='User'):
            req.user_id = token_payload["user_id"]
            match_exact_user_id = True
            
        dataset = data_access.get_roi_income(req=req, match_exact_user_id=match_exact_user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }
            
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_roi_level_income', dependencies=[Depends(RightsChecker([143, 142]))])
def get_roi_level_income(req: GetROILevelIncome_Request, token_payload: any = Depends(get_current_user)):
    try:
        # print(req)
        if(token_payload["role"]=='User'):
            req.user_id = token_payload["user_id"]
            req.match_exact_user_id = True
            
        dataset = data_access.get_roi_level_income(req=req, match_exact_user_id=req.match_exact_user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }
            
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_roi_level_income_concise', dependencies=[Depends(RightsChecker([144, 145]))])
def get_roi_level_income_concise(user_id: str, token_payload: any = Depends(get_current_user)):
    try:
        if(token_payload["role"]=='User'):
            user_id = token_payload["user_id"]
            
        dataset = data_access.get_roi_level_income_concise(user_id=user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'settings': dataFrameToJsonObject(dataset['rs1']) }
            
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
