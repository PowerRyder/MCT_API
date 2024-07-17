
from src.schemas.Wallet import WalletBalanceRequest, WalletCreditDebit, WalletTransactionsRequest
from src.utilities.utils import execute_query


def get_wallet_balance(req: WalletBalanceRequest, match_exact_user_id: bool):
    res = execute_query("call usp_get_wallet_balance(_user_id => %s, _user_type => %s, _match_exact_user_id => %s, _wallet_id => %s, _page_index => %s, _page_size => %s)", 
                        (req.user_id, req.user_type, match_exact_user_id, req.wallet_id, req.page_index, req.page_size))
    return res


def get_wallet_transactions(req: WalletTransactionsRequest):
    res = execute_query("call usp_get_wallet_transactions(_user_id => %s, _user_type => %s, _between_date => %s::timestamptz[], _wallet_id => %s, _type => %s, _search_term => %s, _page_index =>%s, _page_size => %s)",
                        (req.user_id, req.user_type, [req.date_from if req.date_from!='' else None, req.date_to if req.date_to!='' else None], req.wallet_id, req.type, req.search_term, req.page_index, req.page_size))
    return res


def credit_debit(req: WalletCreditDebit, by_admin_user_id: str):
    res = execute_query("call usp_credit_debit(_user_id => %s, _user_type => %s, _wallet_id => %s, _action => %s, _amount => %s, _by_admin_user_id => %s, _remarks => %s)", 
                        (req.user_id, req.user_type, req.wallet_id, req.action, req.amount, by_admin_user_id, req.remarks))
    return res


