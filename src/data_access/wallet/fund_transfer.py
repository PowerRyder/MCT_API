from src.schemas.Wallet import TransferFundHistoryRequest, WalletTransferFund
from src.utilities.utils import execute_query


def transfer_fund(req: WalletTransferFund, by_user_id: str, by_user_type: str):
    res = execute_query("call usp_transfer_fund(_from_user_id => %s, _from_user_type => %s, _from_wallet_id => %s, _to_user_id => %s, _to_user_type => %s, _to_wallet_id => %s, _amount => %s, _remarks => %s, _by_user_id => %s, _by_user_type => %s, _two_factor_auth_request_id => %s)", 
                        (req.from_user_id, req.from_user_type, req.from_wallet_id, req.to_user_id, req.to_user_type, req.to_wallet_id, req.amount, req.remarks, by_user_id, by_user_type, req.two_factor_auth_request_id))
    return res

def fund_transfer_history(req: TransferFundHistoryRequest, match_exact_from_user_id: bool, match_exact_to_user_id: bool):
    res = execute_query("call usp_get_fund_transfer_details(_from_user_id => %s, _from_user_type => %s, _from_wallet_id => %s, _match_exact_from_user_id => %s, _to_user_id => %s, _to_user_type => %s, _to_wallet_id => %s, _match_exact_to_user_id => %s, _between_date => %s::timestamptz[], _remarks => %s, _page_index => %s, _page_size => %s)", 
                        (req.from_user_id, req.from_user_type, req.from_wallet_id, match_exact_from_user_id, req.to_user_id, req.to_user_type, req.to_wallet_id, match_exact_to_user_id, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.remarks, req.page_index, req.page_size))
    return res
