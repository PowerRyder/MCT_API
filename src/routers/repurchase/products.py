from fastapi import APIRouter, Depends
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.repurchase import products as data_access
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.Repurchase import AddUpdateProduct_Request, GetProducts_Request
from src.utilities.utils import get_error_message, dataFrameToJsonObject, save_base64_file

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post('/add_or_update_product', dependencies=[Depends(RightsChecker([188]))])
def add_or_update_product(req: AddUpdateProduct_Request, token_payload: any = Depends(get_current_user)):
    try:
        if req.product_image != '':
            req.product_image, path = save_base64_file(req.product_image, upload_file_name='Product')

        dataset = data_access.add_or_update_product(req=req, added_by_admin_id=token_payload["user_id"])

        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_products', dependencies=[Depends(RightsChecker([189, 194, 195, 196]))])
def get_products(req: GetProducts_Request, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_products(req=req)

        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.delete('/delete_product', dependencies=[Depends(RightsChecker([190]))])
def delete_product(product_id: int, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.delete_product(product_id=product_id, admin_user_id=token_payload["user_id"])

        if len(dataset) > 0:
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

