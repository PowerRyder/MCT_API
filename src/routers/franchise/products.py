
from fastapi import APIRouter, Depends
from src.misc.constants.messages import INVALID_USER_ID, OK, DATABASE_CONNECTION_ERROR
from src.data_access.franchise import products as data_access
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.Franchise import GetFranchiseProducts_Request, GetFranchiseProductStockTransactions_Request
from src.utilities.utils import dataFrameToJsonObject, get_error_message, save_base64_file

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post('/get_franchise_products', dependencies=[Depends(RightsChecker([210, 211, 212, 213]))])
def get_franchise_products(req: GetFranchiseProducts_Request, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if token_payload["role"] != 'Admin':
            req.franchise_id = token_payload["user_id"]
            match_exact_user_id = True

        dataset = data_access.get_franchise_products(req=req, match_exact_user_id=match_exact_user_id)

        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_franchise_product_stock_transactions', dependencies=[Depends(RightsChecker([210, 211, 212, 213]))])
def get_franchise_product_stock_transactions(req: GetFranchiseProductStockTransactions_Request, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if token_payload["role"] != 'Admin':
            req.franchise_id = token_payload["user_id"]
            match_exact_user_id = True

        print(req)

        dataset = data_access.get_franchise_product_stock_transactions(req=req, match_exact_user_id=match_exact_user_id)

        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
