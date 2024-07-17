from fastapi import APIRouter, Depends
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.repurchase import categories as data_access
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.Repurchase import AddCategory_Request, GetCategories_Request, UpdateCategory_Request
from src.utilities.utils import get_error_message, dataFrameToJsonObject

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post('/add_category', dependencies=[Depends(RightsChecker([187]))])
def add_category(req: AddCategory_Request, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.add_category(req=req, added_by_admin_id=token_payload["user_id"])

        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_categories', dependencies=[Depends(RightsChecker([187, 190, 194, 195, 196]))])
def get_categories(req: GetCategories_Request, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_categories(req=req)

        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.put('/update_category', dependencies=[Depends(RightsChecker([187, 190]))])
def update_category(req: UpdateCategory_Request, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.update_category(req=req, admin_user_id=token_payload["user_id"])

        if len(dataset) > 0:
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.delete('/delete_category', dependencies=[Depends(RightsChecker([190]))])
def delete_category(category_id: int, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.delete_category(category_id=category_id, admin_user_id=token_payload["user_id"])

        if len(dataset) > 0:
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

