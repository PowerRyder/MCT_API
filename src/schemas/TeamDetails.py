
from pydantic import BaseModel

from src.misc.constants import VALIDATORS


class DirectDetailsRequest(BaseModel):
    sponsor_id: str = VALIDATORS.USER_ID
    direct_id_name_email_mobile: str
    side: str
    active_status: str
    joining_date_from: str=''
    joining_date_to: str=''
    page_index: int
    page_size: int
    

class DownlineDetailsRequest(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    downline_id_name_email_mobile: str
    side: str
    level: int
    active_status: str
    joining_date_from: str=''
    joining_date_to: str=''
    page_index: int
    page_size: int
    
class DayWiseBusinessDetailsRequest(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    date_from: str=''
    date_to: str=''
    page_index: int
    page_size: int


class GetMatrixMembers(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    pool_id: int
    matrix_id: int
    downline_user_id: str
    level: int
    date_from: str = ''
    date_to: str = ''
    page_index: int
    page_size: int