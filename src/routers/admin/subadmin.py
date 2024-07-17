
from fastapi import APIRouter, Depends
from src.misc.constants.messages import OK
from src.data_access.admin import subadmin as data_access
from src.schemas.Admin import AddNewAdminRequest, AdminAccessRightsUpdateRequest
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.utilities.utils import dataFrameToJsonObject, get_error_message


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get('/get_sub_admins', dependencies=[Depends(RightsChecker([20]))])
def get_sub_admins(token_payload:any = Depends(get_current_user)):
    try:
        by_admin_id = token_payload["user_id"]
        
        dataset = data_access.get_sub_admin(by_admin_user_id=by_admin_id)
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds) }

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/add_new_admin', dependencies=[Depends(RightsChecker([20,21]))])
def add_new_admin(req: AddNewAdminRequest, token_payload:any = Depends(get_current_user)):
    try:
        by_admin_id = token_payload["user_id"]

        dataset = data_access.add_new_admin(admin_user_id=req.admin_user_id, password=req.password, email_id=req.email_id, mobile_no=req.mobile_no, by_admin_user_id=by_admin_id)
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"] }
            
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.put('/update_access_rights', dependencies=[Depends(RightsChecker([20,23]))])
def update_access_rights(req: AdminAccessRightsUpdateRequest, token_payload:any = Depends(get_current_user)):
    try:
        by_admin_id = token_payload["user_id"]

        dataset = data_access.update_admin_access_rights(admin_user_id=req.user_id, access_rights=req.access_rights, by_admin_user_id=by_admin_id)
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"] }
            
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.delete('/delete_admin', dependencies=[Depends(RightsChecker([20]))])
def delete_admin(admin_id: str, token_payload:any = Depends(get_current_user)):
    try:
        by_admin_id = token_payload["user_id"]

        dataset = data_access.delete_admin(admin_user_id=admin_id, by_admin_user_id=by_admin_id)
        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"] }
            
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
