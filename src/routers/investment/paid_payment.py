
from datetime import datetime
import os
from fastapi import APIRouter, Depends, File, UploadFile
from src.misc.security.RightsChecker import RightsChecker
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, UNSUPPORTED_FILE_FORMAT
from src.data_access.investment import paid_payment as data_access
from src.misc.security.Jwt import get_current_user
from src.schemas.Investment import PaymentInfo
from src.utilities.utils import get_error_message, save_base64_file
from src.misc.constants import VALIDATORS
from src.utilities.aes import aes


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post('/insert_paid_payment_details', dependencies=[Depends(RightsChecker([56, 68]))])
async def insert_paid_payment_details(req: PaymentInfo, token_payload: any = Depends(get_current_user)):
    try:
        user_id = token_payload["user_id"]
        user_type = token_payload["role"]

        image_name = ''
        if req.image != '':
            image_name, path = save_base64_file(req.image, upload_file_name='Payment_Receipt')

            dataset = data_access.insert_paid_payment_details(user_id=user_id, user_type=user_type, amount=req.amount,
                                                              payment_mode=req.payment_mode,
                                                              reference_number=req.reference_number, remarks=req.remarks,
                                                              image_path=image_name)
            if len(dataset) > 0 and len(dataset['rs']):
                ds = dataset['rs']
                if (ds.iloc[0].loc["success"]):
                    return {'success': True, 'message': ds.iloc[0].loc["message"],
                            'request_id': aes.encrypt(str(int(ds.iloc[0].loc["request_id"])))}

                return {'success': False, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
        return {'success': False, 'message': UNSUPPORTED_FILE_FORMAT}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

