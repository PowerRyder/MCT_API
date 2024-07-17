
from fastapi import APIRouter, Depends
from src.misc.constants.messages import INVALID_USER_ID, OK, DATABASE_CONNECTION_ERROR
from src.data_access.franchise import profile as data_access
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.Franchise import FranchiseOfficeDetailsUpdate_Request, FranchiseOwnerDetailsUpdate_Request, \
    FranchiseLegalDetailsUpdate_Request, FranchiseBankDetailsUpdate_Request
from src.utilities.utils import dataFrameToJsonObject, get_error_message, save_base64_file

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post('/update_franchise_office_address', dependencies=[Depends(RightsChecker([179, 180]))])
def update_franchise_office_address(req: FranchiseOfficeDetailsUpdate_Request, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.update_franchise_office_address(req=req, by_user_id=token_payload["user_id"], by_user_type=token_payload["role"])
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/update_franchise_owner_details', dependencies=[Depends(RightsChecker([179, 180]))])
def update_franchise_owner_details(req: FranchiseOwnerDetailsUpdate_Request, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.update_franchise_owner_details(req=req, by_user_id=token_payload["user_id"], by_user_type=token_payload["role"])
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/update_franchise_legal_details', dependencies=[Depends(RightsChecker([179, 180]))])
def update_franchise_legal_details(req: FranchiseLegalDetailsUpdate_Request, token_payload: any = Depends(get_current_user)):
    try:
        if req.pan_card_image != '':
            req.pan_card_image, path = save_base64_file(req.pan_card_image, upload_file_name='Franchise_PAN')

        dataset = data_access.update_franchise_legal_details(req=req, by_user_id=token_payload["user_id"], by_user_type=token_payload["role"])
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/update_franchise_bank_details', dependencies=[Depends(RightsChecker([179, 180]))])
def update_franchise_bank_details(req: FranchiseBankDetailsUpdate_Request, token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.update_franchise_bank_details(req=req, by_user_id=token_payload["user_id"], by_user_type=token_payload["role"])
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

