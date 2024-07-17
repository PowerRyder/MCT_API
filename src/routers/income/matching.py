from fastapi import APIRouter, Depends
from src.data_access.income import matching as data_access
from src.misc.constants.messages import (DATABASE_CONNECTION_ERROR, OK)
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.Income import GetMatchingIncome_Request, GetMatchingBusinessDetails_Request, \
    GetMatchingLevelIncome_Request
from src.utilities.utils import dataFrameToJsonObject, get_error_message

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get('/get_matching_payouts', dependencies=[Depends(RightsChecker([132, 133]))])
def get_matching_payouts():
    try:
        dataset = data_access.get_matching_payouts()
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds)}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_matching_types', dependencies=[Depends(RightsChecker([132, 133]))])
def get_matching_types():
    try:
        dataset = data_access.get_matching_types()
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds)}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_matching_income', dependencies=[Depends(RightsChecker([132, 133]))])
def get_matching_income(req: GetMatchingIncome_Request, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if (token_payload["role"] == 'User'):
            req.user_id = token_payload["user_id"]
            match_exact_user_id = True

        dataset = data_access.get_matching_income(req=req, match_exact_user_id=match_exact_user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_matching_business_details', dependencies=[Depends(RightsChecker([132, 133]))])
def get_matching_business_details(req: GetMatchingBusinessDetails_Request, token_payload: any = Depends(get_current_user)):
    try:
        if (token_payload["role"] == 'User'):
            req.user_id = token_payload["user_id"]

        dataset = data_access.get_matching_business_details(req=req)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_matching_level_income', dependencies=[Depends(RightsChecker([160, 161]))])
def get_matching_level_income(req: GetMatchingLevelIncome_Request, token_payload: any = Depends(get_current_user)):
    try:
        # print(req)
        if (token_payload["role"] == 'User'):
            req.user_id = token_payload["user_id"]
            req.match_exact_user_id = True

        dataset = data_access.get_matching_level_income(req=req, match_exact_user_id=req.match_exact_user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_matching_level_income_concise', dependencies=[Depends(RightsChecker([162, 163]))])
def get_matching_level_income_concise(user_id: str, payout_no: int=0, binary_type_id: int=0, token_payload: any = Depends(get_current_user)):
    try:
        if (token_payload["role"] == 'User'):
            user_id = token_payload["user_id"]

        dataset = data_access.get_matching_level_income_concise(user_id=user_id, payout_no=payout_no, binary_type_id=binary_type_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds),
                    'settings': dataFrameToJsonObject(dataset['rs1'])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
