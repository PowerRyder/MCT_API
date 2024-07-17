
from fastapi import APIRouter, Depends
from src.data_access.admin import profile as data_access
from src.schemas.Admin import AdminDetailsUpdateRequest
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.utilities.utils import get_error_message
from src.utilities.aes import aes


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.put('/update_details', dependencies=[Depends(RightsChecker([16, 20]))]) # for self profile update or subadmin profile update
def update_details(req: AdminDetailsUpdateRequest, token_payload:any = Depends(get_current_user)):
    try:
        by_admin_user_id = token_payload["user_id"]

        if(req.two_factor_auth_request_id!=''):
            req.two_factor_auth_request_id = int(aes.decrypt(req.two_factor_auth_request_id))
        else:
            req.two_factor_auth_request_id = 0
            
        dataset = data_access.update_admin_details(user_id=req.user_id, email_id=req.email_id, mobile_no=req.mobile_no, by_admin_user_id=by_admin_user_id, two_factor_auth_request_id=req.two_factor_auth_request_id)
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"] }
            
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
