from fastapi import APIRouter, Depends
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.repurchase import product_stocks as data_access
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.Repurchase import AddProductStock_Request, GetProductStockTransactions_Request
from src.utilities.utils import get_error_message, dataFrameToJsonObject

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post('/add_product_stock', dependencies=[Depends(RightsChecker([192]))])
def add_product_stock(req: AddProductStock_Request, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.add_product_stock(req=req, added_by_admin_id=token_payload["user_id"])

        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_product_stock_transactions', dependencies=[Depends(RightsChecker([193]))])
def get_product_stock_transactions(req: GetProductStockTransactions_Request, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_product_stock_transactions(req=req)

        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
