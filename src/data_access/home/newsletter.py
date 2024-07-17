
from src.utilities.utils import execute_query


def newsletter_subscription(email: str, subscription_status: bool):
    res = execute_query("call usp_subscribe_newsletter(_email => %s, _subscription_status => %s)", (email, subscription_status))
    return res