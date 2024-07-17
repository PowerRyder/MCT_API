from fastapi import APIRouter, Depends
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, INVALID_USER_ID, OK
from src.misc.security.Jwt import get_current_user
from src.data_access.team import matrix as data_access
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.TeamDetails import GetMatrixMembers
from src.utilities.utils import dataFrameToJsonObject, get_error_message

router = APIRouter(
    tags=["Matrix"]
)


@router.get('/get_pools', dependencies=[Depends(RightsChecker([52, 53, 54, 55])), Depends(get_current_user)])
def get_pools():
    try:
        dataset = data_access.get_pools()
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds)}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

@router.get('/get_pool_entry_ids', dependencies=[Depends(RightsChecker([52, 53, 54, 55])), Depends(get_current_user)])
def get_pool_entry_ids(user_id: str, pool_id: int):
    try:
        dataset = data_access.get_pool_entry_ids(user_id=user_id, pool_id=pool_id)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds)}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_matrix_members', dependencies=[Depends(RightsChecker([31, 34])), Depends(get_current_user)])
def get_matrix_members(req: GetMatrixMembers, token_payload: any = Depends(get_current_user)):
    try:
        if(token_payload["role"]!='Admin'):
            req.user_id = token_payload["user_id"]

        dataset = data_access.get_matrix_members(req)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

