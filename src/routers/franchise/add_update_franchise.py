
from fastapi import APIRouter, Depends
from src.misc.constants.messages import INVALID_USER_ID, OK, DATABASE_CONNECTION_ERROR
from src.data_access.franchise import add_update_franchise as data_access
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.Franchise import AddFranchise_Request, FranchiseList_Request, FranchiseAccessRightsUpdateRequest
from src.utilities.utils import dataFrameToJsonObject, get_error_message, save_base64_file

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post('/add_franchise', dependencies=[Depends(RightsChecker([176, 178]))])
def add_franchise(req: AddFranchise_Request, token_payload: any = Depends(get_current_user)):
    try:
        if token_payload["role"] != 'Admin':
            req.master_franchise_user_id = token_payload["user_id"]
            req.is_master_franchise = False

        req.pan_card_image, path = save_base64_file(req.pan_card_image, upload_file_name='Franchise_PAN')

        dataset = data_access.add_franchise(req=req, added_by_user_id=token_payload["user_id"], added_by_user_type=token_payload["role"])
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_franchise_list', dependencies=[Depends(RightsChecker([179, 180])), Depends(get_current_user)])
def get_franchise_list(req: FranchiseList_Request, token_payload: any = Depends(get_current_user)):
    try:
        if token_payload["role"] != 'Admin':
            req.master_franchise_user_id = token_payload["user_id"]

        dataset = data_access.get_franchise_list(req)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/toggle_franchise_block_unblock', dependencies=[Depends(RightsChecker([179, 180]))])
def toggle_franchise_block_unblock(user_id: str, token_payload: any = Depends(get_current_user)):
    try:
        # print(req)
        by_user_id = token_payload["user_id"]
        dataset = data_access.toggle_franchise_block_unblock(user_id=user_id, by_user_id=by_user_id)

        if len(dataset) > 0:
            ds = dataset['rs']
            if (ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_master_franchise_access_rights_for_admin', dependencies=[Depends(RightsChecker([180, 181]))])
def get_master_franchise_access_rights_for_admin():
    try:
        dataset = data_access.get_master_franchise_access_rights_for_admin()

        if len(dataset) > 0:
            ds = dataset['rs']
            if (ds.iloc[0].loc["success"]):
                return {'success': True, 'message': OK, 'access_rights': ds.iloc[0].loc["access_rights"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.put('/update_access_rights', dependencies=[Depends(RightsChecker([179, 180]))])
def update_access_rights(req: FranchiseAccessRightsUpdateRequest, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.update_franchise_access_rights(user_id=req.user_id, access_rights=req.access_rights, by_user_id=token_payload["user_id"], by_user_type=token_payload["role"])
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

