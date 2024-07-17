
from fastapi import APIRouter, Depends
from src.misc.constants import VALIDATORS
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, INVALID_USER_ID, OK
from src.data_access.team import tree as data_access
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.utilities.utils import dataFrameToJsonObject, get_error_message


router = APIRouter(
    tags=["Tree"]
)

@router.get('/binary_tree', dependencies=[Depends(RightsChecker([40, 41])), Depends(get_current_user)])
def binary_tree(searched_user_id: str = VALIDATORS.DEFAULT, token_payload: any = Depends(get_current_user)):
    try:
        user_id = ''
        if token_payload["role"] != "Admin":
            user_id = token_payload["user_id"]

        # print(user_id, searched_user_id)
        dataset = data_access.getBinaryTree(user_id=user_id, searched_user_id=searched_user_id)
        if len(dataset) > 0:
            ds = dataset['rs']

            if (ds.iloc[0].loc["valid"]):
                return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(dataset['rs_tree_data'])}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/direct_tree', dependencies=[Depends(RightsChecker([42, 43])), Depends(get_current_user)])
def direct_tree(searched_user_id: str = VALIDATORS.DEFAULT, token_payload: any = Depends(get_current_user)):
    try:
        user_id = ''
        if token_payload["role"] != "Admin":
            user_id = token_payload["user_id"]
        # print(user_id, searched_user_id)
        dataset = data_access.getDirectTree(user_id=user_id, searched_user_id=searched_user_id)
        if len(dataset) > 0:
            ds = dataset['rs']

            if (ds.iloc[0].loc["valid"]):
                return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(dataset['rs_tree_data'])}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/matrix_tree', dependencies=[Depends(RightsChecker([159, 158])), Depends(get_current_user)])
def matrix_tree(user_id: str, pool_id: int, matrix_id: int, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.getMatrixTree(user_id=user_id, pool_id=pool_id, matrix_id=matrix_id)
        if len(dataset)>0:
            ds = dataset['rs']

            if (ds.iloc[0].loc["valid"]):
                return { 'success': True, 'message': OK, 'data': dataFrameToJsonObject(dataset['rs_tree_data']) }

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
