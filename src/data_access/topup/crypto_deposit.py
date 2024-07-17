from src.schemas.Topup import GetCryptoDeposit
from src.utilities.utils import execute_query


def save_crypto_deposit_request_details(user_id: str, network: str, token_symbol: str, payment_request_id: str, amount: float):
    res = execute_query("call usp_save_crypto_deposit_request_details(_user_id => %s, _network => %s, _token_symbol => %s, _payment_request_id => %s, _amount => %s)",
                        (user_id, network, token_symbol, payment_request_id, amount))
    return res


def update_crypto_deposit_request_details(payment_request_id: str, input_txn_hash: str, input_txn_explorer_url: str,
                                          in_amount: float, input_txn_status: str, input_txn_timestamp: int,
                                          out_transaction_hash: str, output_txn_explorer_url: str,
                                          out_transaction_status: str, out_transaction_date: int, out_amount: float,
                                          out_processing_fee: float):
    res = execute_query("call usp_update_crypto_deposit_transaction_details(_payment_request_id => %s, "
                        "_input_txn_hash => %s, _input_txn_hash_explorer_url => %s, _input_amount => %s, "
                        "_input_txn_status => %s, _input_txn_timestamp => %s,"
                        "_out_transaction_hash => %s, _output_txn_hash_explorer_url => %s, "
                        "_out_transaction_status => %s, _out_transaction_date => %s, "
                        "_out_amount => %s, _out_processing_fee => %s)",
                        (payment_request_id, input_txn_hash, input_txn_explorer_url, in_amount, input_txn_status,
                         input_txn_timestamp, out_transaction_hash, output_txn_explorer_url, out_transaction_status,
                         out_transaction_date, out_amount, out_processing_fee))
    return res


def get_crypto_deposit_request_details(request_id: int):
    res = execute_query("call usp_get_crypto_deposit_request_details(_request_id => %s)",
                        (request_id, ))
    return res


def get_crypto_deposits_history(req: GetCryptoDeposit, match_exact_user_id: bool = False):
    res = execute_query("call usp_get_crypto_deposits_history(_user_id => %s, _match_exact_user_id => %s, _between_date => %s::timestamptz[], _request_id => %s, _txn_hash => %s, _input_txn_status => %s, _page_index => %s, _page_size => %s)",
                        (req.user_id, match_exact_user_id, [req.date_from if req.date_from != '' else None, req.date_to if req.date_to != '' else None], req.request_id, req.txn_hash, req.input_txn_status, req.page_index, req.page_size))
    return res

