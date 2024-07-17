from fastapi import APIRouter, Depends
from src.data_access.income import weekly_bonus as data_access
from src.misc.constants.messages import (DATABASE_CONNECTION_ERROR, OK)
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.Income import GetWeeklyBonusIncome_Request
from src.utilities.utils import dataFrameToJsonObject, get_error_message

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get('/get_weekly_bonus_payouts', dependencies=[Depends(RightsChecker([216, 218]))])
def get_weekly_bonus_payouts():
    try:
        dataset = data_access.get_weekly_bonus_payouts()
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds)}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_weekly_bonus_income', dependencies=[Depends(RightsChecker([216, 218]))])
def get_weekly_bonus_income(req: GetWeeklyBonusIncome_Request, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if (token_payload["role"] == 'User'):
            req.user_id = token_payload["user_id"]
            match_exact_user_id = True

        dataset = data_access.get_weekly_bonus_income(req=req, match_exact_user_id=match_exact_user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
