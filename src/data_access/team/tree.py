
from src.utilities.utils import execute_query


def getBinaryTree(user_id: str, searched_user_id: str):
    res = execute_query("call usp_get_binary_tree(_upline_user_id => %s, _searched_user_id => %s)", (user_id, searched_user_id))
    return res


def getDirectTree(user_id: str, searched_user_id: str):
    res = execute_query("call usp_get_direct_tree(_user_id => %s, _searched_user_id => %s)", (user_id, searched_user_id))
    return res


def getMatrixTree(user_id: str, pool_id: int, matrix_id: int):
    res = execute_query("call usp_get_matrix_tree(_user_id => %s, _pool_id => %s, _matrix_id => %s)",
                        (user_id, pool_id, matrix_id))
    return res
