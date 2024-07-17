

from fastapi import APIRouter, Depends
from src.schemas.VirtualBusiness import AddVirtualBusinessRequest, GetVirtualBusinessRequest
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.admin.miscellaneous import virtual_business as data_access
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.utilities.utils import dataFrameToJsonObject, get_error_message


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.post('/add_virtual_business', dependencies=[Depends(RightsChecker([38]))])
def add_virtual_business(req: AddVirtualBusinessRequest, token_payload:any = Depends(get_current_user)):
    try:
        by_admin_id = token_payload["user_id"]
        
        dataset = data_access.insert_virtual_business(req=req, admin_user_id=by_admin_id)
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"] }
        
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
        
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

@router.post('/get_virtual_business', dependencies=[Depends(RightsChecker([39]))])
def get_virtual_business(req: GetVirtualBusinessRequest, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False

        if(token_payload["role"]!="Admin"):
            match_exact_user_id = True

        dataset = data_access.get_virtual_business(req=req, match_exact_user_id=match_exact_user_id)
        if len(dataset)>0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }
        
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_total_matching_business', dependencies=[Depends(RightsChecker([38]))])
def get_total_matching_business(user_id: str, binary_type_id: int):
    try:
        dataset = data_access.get_total_matching_business(user_id=user_id, binary_type_id=binary_type_id)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds)}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
