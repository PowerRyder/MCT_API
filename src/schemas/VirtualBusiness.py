
from pydantic import BaseModel
from src.misc.constants import VALIDATORS


class AddVirtualBusinessRequest(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    binary_type_id: int = 0
    amount: float = VALIDATORS.REQUIRED
    point_value: float = VALIDATORS.REQUIRED
    side: str = VALIDATORS.SIDE
    remarks: str
    

class GetVirtualBusinessRequest(BaseModel):
    user_id: str
    date_from: str=''
    date_to: str=''
    binary_type_id: int = 0
    page_index: int
    page_size: int
