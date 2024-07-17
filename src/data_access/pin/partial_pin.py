

from src.schemas.Pin import PayPartialPinAmountRequest
from src.utilities.utils import execute_query


def pay_partial_pin_amount(req: PayPartialPinAmountRequest, admin_user_id: str):
    res = execute_query("call usp_pay_pin_balance(_admin_user_id => %s, _pin_number => %s, _pin_password => %s, _amount => %s, _remarks => %s)", (admin_user_id, req.pinNumber, req.pinPassword, req.amount, req.remarks))
    return res
