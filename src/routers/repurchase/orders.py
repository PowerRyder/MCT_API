from fastapi import APIRouter, Depends
from src.utilities.aes import aes
from src.misc.constants import VALIDATORS
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.repurchase import orders as data_access
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.Repurchase import AddUpdateProduct_Request, AddShippingAddress, PlaceRepurchaseOrder, \
    GetRepurchaseOrders, RepurchaseOrderDispatchStatusUpdateRequest
from src.utilities.utils import get_error_message, dataFrameToJsonObject

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get('/get_shipping_addresses', dependencies=[Depends(RightsChecker([194, 195, 196]))])
def get_shipping_addresses(user_id: str, user_type: str = VALIDATORS.USER_TYPE, token_payload: any = Depends(get_current_user)):
    try:
        if token_payload["role"] == 'User':
            user_id = token_payload["user_id"]
            user_type = token_payload["role"]

        dataset = data_access.get_shipping_addresses(user_id=user_id, user_type=user_type)

        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"], 'name': ds.iloc[0].loc["name"], 'data': dataFrameToJsonObject(dataset['rs_shipping_addresses'])}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/add_shipping_address', dependencies=[Depends(RightsChecker([194, 195, 196]))])
def add_shipping_address(req: AddShippingAddress, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.add_shipping_address(req=req, added_by_id=token_payload["user_id"], add_by_user_type=token_payload["role"])

        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}



@router.post('/place_repurchase_order', dependencies=[Depends(RightsChecker([194, 195, 196]))])
def place_repurchase_order(req: PlaceRepurchaseOrder, token_payload: any = Depends(get_current_user)):
    try:
        if(req.payment_id!=''):
            req.payment_id = aes.decrypt(req.payment_id)
        else:
            req.payment_id = 0

        dataset = data_access.place_repurchase_order(req=req, by_id=token_payload["user_id"], by_user_type=token_payload["role"])

        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_repurchase_orders', dependencies=[Depends(RightsChecker([205, 206, 207]))])
def get_repurchase_orders(req: GetRepurchaseOrders, token_payload: any = Depends(get_current_user)):
    try:
        print(req)
        match_exact_user_id = False
        match_exact_franchise_id = False
        do_not_include_self_orders = False
        if token_payload["role"] == 'User':
            req.user_id = token_payload["user_id"]
            req.user_type = token_payload["role"]
            match_exact_user_id = True

        elif token_payload["role"] == 'Franchise':
            if req.type == 'To Me':
                req.user_id = token_payload["user_id"]
                req.user_type = token_payload["role"]
                match_exact_user_id = True
            else:
                req.by_franchise_id = token_payload["user_id"]
                do_not_include_self_orders = True
                match_exact_franchise_id = True

        dataset = data_access.get_repurchase_orders(req=req, match_exact_user_id=match_exact_user_id, match_exact_franchise_id=match_exact_franchise_id, do_not_include_self_orders=do_not_include_self_orders)

        if len(dataset) > 0:
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(dataset['rs']), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_repurchase_order_details', dependencies=[Depends(RightsChecker([194, 195, 196]))])
def get_repurchase_order_details(order_id: int, page_index: int = 0, page_size: int = 100, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_repurchase_order_details(order_id=order_id, page_index=page_index, page_size=page_size)

        if len(dataset) > 0:
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(dataset['rs']), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.put('/mark_order_as_paid', dependencies=[Depends(RightsChecker([194, 195, 196]))])
def mark_order_as_paid(order_id: int, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.mark_order_as_paid(order_id=order_id, by_id=token_payload["user_id"], by_user_type=token_payload["role"])

        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.put('/update_order_dispatch_status', dependencies=[Depends(RightsChecker([205, 207]))])
async def update_order_dispatch_status(req: RepurchaseOrderDispatchStatusUpdateRequest, token_payload: any = Depends(get_current_user)):
    try:
        by_user_id = token_payload["user_id"]
        by_user_type = token_payload["role"]
        # print(req)
        dataset = data_access.update_order_dispatch_status(req=req, by_user_id=by_user_id, by_user_type=by_user_type)
        if len(dataset) > 0:
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"] }

            return {'success': False, 'message': ds.iloc[0].loc["message"] }

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
