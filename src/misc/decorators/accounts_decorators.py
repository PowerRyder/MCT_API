
from functools import wraps

from fastapi import HTTPException
from src.utilities.aes import aes
from src.data_access.accounts import login as data_access


def is_valid_login_id(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        try:
            login_id = aes.decrypt(kwargs['login_id'])
            dataset_validity = data_access.isValidLoginId(user_id=kwargs['user_id'], login_id=login_id)

            if len(dataset_validity)>0 and len(dataset_validity['rs']):
                ds_validity = dataset_validity['rs']
                # print(ds.iloc[0].loc['valid'])
                if(ds_validity.iloc[0].loc['valid']):
                    return func(*args, **kwargs)

            raise HTTPException(status_code=403, detail="Operation not permitted")
        except Exception as e:
            print(e.__str__())
            raise HTTPException(status_code=403, detail="Operation not permitted")

    return wrapper
