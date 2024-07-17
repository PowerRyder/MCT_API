from src.schemas.Admin import ExecuteTrade
from src.utilities.utils import execute_query


def get_trade_pairs(type, trade_pairs):
    res = execute_query("call usp_get_trade_pairs(_type => %s, _trade_pairs => %s)", (type, trade_pairs))
    return res


def save_trade(req: ExecuteTrade):
    res = execute_query("call usp_save_trade(_type => %s, _base_currency => %s, _quote_currencies => %s, _profit_percentage => %s, _trade_amount => %s)",
                        (req.type, req.base_currency, req.quote_currencies, req.profit_percentage, req.trade_amount))
    return res


def get_trades(user_id, page_index, page_size):
    res = execute_query("call usp_get_trades_history(_user_id => %s, _page_index => %s, _page_size => %s)", (user_id, page_index, page_size))
    return res


def get_trade_details(trade_id, user_id):
    res = execute_query("call usp_get_trade_details(_trade_id => %s, _user_id => %s)", (trade_id, user_id))
    return res
