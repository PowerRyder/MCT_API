from fastapi import APIRouter, Depends

from src.data_access.income import total as data_access
from src.misc.constants.messages import (DATABASE_CONNECTION_ERROR, OK)
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.Income import GetAllIncome_Request, GetTotalIncome_Request, PayPayoutAmount_Request
from src.utilities.utils import dataFrameToJsonObject, get_error_message

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post('/get_all_income', dependencies=[Depends(RightsChecker([10, 11]))])
def get_all_income(req: GetAllIncome_Request, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if token_payload["role"] == 'User':
            req.user_id = token_payload["user_id"]
            match_exact_user_id = True

        dataset = data_access.get_all_income(req=req, match_exact_user_id=match_exact_user_id)
        # print(req, dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_total_income_payouts', dependencies=[Depends(RightsChecker([170, 171]))])
def get_total_income_payouts():
    try:
        dataset = data_access.get_total_income_payouts()
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds)}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_total_income', dependencies=[Depends(RightsChecker([170, 171]))])
def get_total_income(req: GetTotalIncome_Request, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if (token_payload["role"] == 'User'):
            req.user_id = token_payload["user_id"]
            match_exact_user_id = True

        dataset = data_access.get_total_income(req=req, match_exact_user_id=match_exact_user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_user_total_payout_payment_amount', dependencies=[Depends(RightsChecker([170, 171]))])
def get_user_total_payout_payment_amount(user_id: str, payout_no: int, wallet_id: int = 0):
    try:
        dataset = data_access.get_user_total_payout_payment_amount(user_id=user_id, payout_no=payout_no, wallet_id=wallet_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds)}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/pay_payout_amount', dependencies=[Depends(RightsChecker([170]))])
def pay_payout_amount(req: PayPayoutAmount_Request, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.pay_payout_amount(req=req, admin_user_id=token_payload["user_id"])
        # print(dataset)
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"] }

            return {'success': False, 'message': ds.iloc[0].loc["message"] }

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
