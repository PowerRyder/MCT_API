

from fastapi import APIRouter, Depends

from src.misc.constants.messages import OK, DATABASE_CONNECTION_ERROR
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.Admin import ExecuteTrade
from src.utilities.utils import dataFrameToJsonObject, get_error_message
from src.data_access.admin.miscellaneous import trading as data_access

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get('/get_trade_pairs', dependencies=[Depends(RightsChecker([226]))])
def get_trade_pairs(type: str, trade_pair_count: int = 1, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_trade_pairs(type=type, trade_pairs=trade_pair_count)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds)}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/save_trade', dependencies=[Depends(RightsChecker([226]))])
def save_trade(req: ExecuteTrade, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.save_trade(req=req)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': ds.iloc[0].loc['message']}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_trades', dependencies=[Depends(RightsChecker([226, 12]))])
def get_trades(page_index: int = 0, page_size: int = 10, token_payload: any = Depends(get_current_user)):
    try:
        user_id = ''
        if token_payload['role'] == "User":
            user_id = token_payload['user_id']

        dataset = data_access.get_trades(user_id=user_id, page_index=page_index, page_size=page_size)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_trade_details', dependencies=[Depends(RightsChecker([226, 12]))])
def get_trade_details(trade_id: int = 0, token_payload: any = Depends(get_current_user)):
    try:
        user_id = ''
        if token_payload['role'] == "User":
            user_id = token_payload['user_id']

        dataset = data_access.get_trade_details(trade_id=trade_id, user_id=user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds)}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
