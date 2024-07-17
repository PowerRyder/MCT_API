

import io
from fastapi import APIRouter, Depends
from src.schemas.MemberSearch import MemberCountRequest, MemberSearchRequest
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.misc.security.RightsChecker import RightsChecker
from src.data_access.admin import member_search as data_access
from src.misc.security.Jwt import get_current_user
from src.utilities.utils import dataFrameToJsonObject, get_error_message


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.post('/member_search', dependencies=[Depends(RightsChecker([26])), Depends(get_current_user)])
def member_search(req: MemberSearchRequest):
    try:
        print(req)
        dataset = data_access.member_search(req)
        if len(dataset)>0:
            ds = dataset['rs']
            return { 'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }
                
        return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}



@router.post('/member_count', dependencies=[Depends(RightsChecker([26])), Depends(get_current_user)])
def member_search(req: MemberCountRequest):
    try:
        dataset = data_access.member_count(req)
        if len(dataset)>0:
            ds = dataset['rs']
            return { 'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }
                
        return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


# @router.post('/member_search_export_to_csv', dependencies=[Depends(RightsChecker([26])), Depends(get_current_user)])
# def member_search(req: MemberSearchRequest):
#     try:
#         dataset = data_access.member_search(req)
#         if len(dataset)>0:
#             ds = dataset['rs']
                        
#             stream = io.StringIO()
#             ds.to_csv(stream, sep=";",index=False)
#             return { 'success': True, 'message': OK, 'data': stream.getvalue() }
                
#         return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }
#     except Exception as e:
#         print(e.__str__())
#         return {'success': False, 'message': get_error_message(e)}


@router.get('/toggle_member_block_unblock', dependencies=[Depends(RightsChecker([26]))])
def toggle_member_block_unblock(user_id: str, token_payload: any = Depends(get_current_user)):
    try:
        # print(req)
        by_admin_user_id = token_payload["user_id"]
        dataset = data_access.toggle_member_block_unblock(user_id=user_id, admin_user_id=by_admin_user_id)

        if len(dataset)>0:
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                return { 'success': True, 'message': ds.iloc[0].loc["message"] }
                
        return { 'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
