

from fastapi import APIRouter, Depends

from src.misc.constants.messages import OK, DATABASE_CONNECTION_ERROR
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.Income import UpdateROIPercentage_Request
from src.utilities.utils import dataFrameToJsonObject, get_error_message, reload_company_details
from src.data_access.admin.miscellaneous import roi_percentage as data_access

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get('/get_roi_ranks', dependencies=[Depends(RightsChecker([220]))])
def get_roi_ranks(token_payload: any = Depends(get_current_user)):
    try:
        dataset = data_access.get_roi_ranks()
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds)}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.put('/update_roi_percentage', dependencies=[Depends(RightsChecker([220]))])
def update_roi_percentage(req: UpdateROIPercentage_Request, token_payload: any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]

        dataset = data_access.update_roi_rank_percentage(req=req, user_id=user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                reload_company_details()
                return {'success': True, 'message': ds.iloc[0].loc["message"] }

            return {'success': False, 'message': ds.iloc[0].loc["message"] }

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/process_roi', dependencies=[Depends(RightsChecker([220]))])
def process_roi(token_payload: any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]

        dataset = data_access.process_roi(admin_id=user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                return {'success': True, 'message': ds.iloc[0].loc["message"] }

            return {'success': False, 'message': ds.iloc[0].loc["message"] }

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

