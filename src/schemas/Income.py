
from pydantic import BaseModel


class GetReferralIncome_Request(BaseModel):
    user_id: str=''
    from_user_id: str=''
    date_from: str = ''
    date_to: str = ''
    page_index: int = 0
    page_size: int = 100
    

class GetLevelIncome_Request(BaseModel):
    user_id: str=''
    match_exact_user_id: bool=False
    downline_id: str=''
    level: int = 0
    date_from: str = ''
    date_to: str = ''
    package_id: int = 0
    page_index: int = 0
    page_size: int = 100
    
    
class GetRoiIncome_Request(BaseModel):
    user_id: str=''
    date_from: str = ''
    date_to: str = ''
    package_id: int = 0
    page_index: int = 0
    page_size: int = 100


class UpdateROIPercentage_Request(BaseModel):
    rank_id: int
    percentage: float


class GetRankAndRewardIncome_Request(BaseModel):
    user_id: str = ''
    date_from: str = ''
    date_to: str = ''
    rank_id: int = 0
    page_index: int = 0
    page_size: int = 100


class GetROILevelIncome_Request(BaseModel):
    user_id: str=''
    match_exact_user_id: bool=False
    downline_id: str=''
    level: int = 0
    date_from: str = ''
    date_to: str = ''
    package_id: int = 0
    page_index: int = 0
    page_size: int = 100
    roi_id: int = 0


class GetSpillIncome_Request(BaseModel):
    user_id: str = ''
    from_user_id: str = ''
    type: str = 'All'
    date_from: str = ''
    date_to: str = ''
    page_index: int = 0
    page_size: int = 100


class GetSingleLegIncome_Request(BaseModel):
    user_id: str = ''
    match_exact_user_id: bool = False
    downline_id: str = ''
    level: int = 0
    date_from: str = ''
    date_to: str = ''
    package_id: int = 0
    page_index: int = 0
    page_size: int = 100


class GetMatrixIncome_Request(BaseModel):
    user_id: str = ''
    match_exact_user_id: bool = False
    downline_id: str = ''
    level: int = 0
    date_from: str = ''
    date_to: str = ''
    matrix_id: int = 0
    pool_id: int = 0
    page_index: int = 0
    page_size: int = 100


class GetMatchingIncome_Request(BaseModel):
    user_id: str = ''
    payout_no: int = 0
    date_from: str = ''
    date_to: str = ''
    binary_type_id: int = 0
    page_index: int = 0
    page_size: int = 100


class GetWeeklyBonusIncome_Request(BaseModel):
    user_id: str = ''
    payout_no: int = 0
    date_from: str = ''
    date_to: str = ''
    page_index: int = 0
    page_size: int = 100


class GetMonthlyBonus_Request(BaseModel):
    user_id: str = ''
    payout_no: int = 0
    date_from: str = ''
    date_to: str = ''
    page_index: int = 0
    page_size: int = 100


class GetMatchingBusinessDetails_Request(BaseModel):
    user_id: str = ''
    payout_no: int = 0
    binary_type_id: int = 0
    page_index: int = 0
    page_size: int = 100


class GetMatchingLevelIncome_Request(BaseModel):
    user_id: str = ''
    match_exact_user_id: bool = False
    downline_id: str = ''
    level: int = 0
    date_from: str = ''
    date_to: str = ''
    payout_no: int = 0
    binary_type_id: int = 0
    binary_income_id: int = 0
    page_index: int = 0
    page_size: int = 100


class GetWithdrawalLevelIncome_Request(BaseModel):
    user_id: str = ''
    match_exact_user_id: bool = False
    downline_id: str = ''
    level: int = 0
    date_from: str = ''
    date_to: str = ''
    page_index: int = 0
    page_size: int = 100


class GetAllIncome_Request(BaseModel):
    user_id: str = ''
    type: str = 'All'
    date_from: str = ''
    date_to: str = ''
    total_income_payout_no: int = 0
    page_index: int = 0
    page_size: int = 100


class GetTotalIncome_Request(BaseModel):
    user_id: str = ''
    payout_no: int = 0
    wallet_id: int = 0
    date_from: str = ''
    date_to: str = ''
    page_index: int = 0
    page_size: int = 100


class PayPayoutAmount_Request(BaseModel):
    user_id: str
    payout_no: int = 0
    wallet_id: int = 0
    amount: float
    remarks: str = ''


class GetRepurchaseLevelIncome_Request(BaseModel):
    user_id: str = ''
    match_exact_user_id: bool = False
    downline_id: str = ''
    level: int = 0
    date_from: str = ''
    date_to: str = ''
    page_index: int = 0
    page_size: int = 100
