from fastapi import APIRouter, Depends
from src.data_access.user import kyc as data_access
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.schemas.KYC import KYCRequest, GetKYCRequest, KycRequestApproveRejectDataItem
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.utilities.utils import get_error_message, save_base64_file, dataFrameToJsonObject
import json


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post('/request_for_kyc', dependencies=[Depends(RightsChecker([173]))])
def request_for_kyc(req: KYCRequest, token_payload: any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]

        req.aadhaar_front_image, path = save_base64_file(req.aadhaar_front_image, upload_file_name='KYC_Aadhaar_Front')

        req.aadhaar_back_image, path = save_base64_file(req.aadhaar_back_image, upload_file_name='KYC_Aadhaar_Back')

        req.pan_image, path = save_base64_file(req.pan_image, upload_file_name='KYC_PAN')

        dataset = data_access.request_for_kyc(user_id=user_id, req=req)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']

            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}



@router.post('/get_kyc_requests', dependencies=[Depends(RightsChecker([173, 174]))])
def get_kyc_requests(req: GetKYCRequest, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if token_payload["role"] == 'User':
            req.user_id = token_payload["user_id"]
            match_exact_user_id = True

        dataset = data_access.get_kyc_requests(req=req, match_exact_user_id=match_exact_user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.put('/update_kyc_requests_status', dependencies=[Depends(RightsChecker([174]))])
async def update_kyc_requests_status(dataItems: list[KycRequestApproveRejectDataItem], token_payload: any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]

        data_dicts = json.dumps([item.dict() for item in dataItems])
        # print(data_dicts)
        dataset = data_access.update_kyc_requests_status(by_user_id=user_id, data_dicts = data_dicts)
        if len(dataset) > 0:
            ds = dataset['rs']
            if (ds.iloc[0].loc["success"]):
                return {
                    'success': True,
                    'message': ds.iloc[0].loc["message"],
                    'approved_count': int(ds.iloc[0].loc["approved_count"]),
                    'rejected_count': int(ds.iloc[0].loc["rejected_count"])
                }

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

