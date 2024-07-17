from fastapi import APIRouter, Depends
from src.data_access.income import single_leg as data_access
from src.misc.constants.messages import (DATABASE_CONNECTION_ERROR, OK)
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.Income import GetSingleLegIncome_Request
from src.utilities.utils import dataFrameToJsonObject, get_error_message

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post('/get_single_leg_income', dependencies=[Depends(RightsChecker([136, 137, 138, 139]))])
def get_single_leg_income(req: GetSingleLegIncome_Request, token_payload: any = Depends(get_current_user)):
    try:
        if (token_payload["role"] == 'User'):
            req.user_id = token_payload["user_id"]
            req.match_exact_user_id = True

        dataset = data_access.get_single_leg_income(req=req, match_exact_user_id=req.match_exact_user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_single_leg_income_concise', dependencies=[Depends(RightsChecker([138, 139]))])
def get_single_leg_income_concise(user_id: str, token_payload: any = Depends(get_current_user)):
    try:
        if (token_payload["role"] == 'User'):
            user_id = token_payload["user_id"]

        dataset = data_access.get_single_leg_income_concise(user_id=user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'settings': dataFrameToJsonObject(dataset['rs1'])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
