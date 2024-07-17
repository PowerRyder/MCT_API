
from fastapi import APIRouter
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR
from src.data_access.home import newsletter as data_access
from src.utilities.utils import get_error_message


router = APIRouter(
    prefix="/newsletter"
    )

@router.get('/subscribe')
def subscribe(email: str):
    try:
        dataset = data_access.newsletter_subscription(email=email, subscription_status=True)

        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"] }
            
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success' : False, 'message' : get_error_message(e)}
    

@router.get('/unsubscribe')
def unsubscribe(email: str):
    try:
        dataset = data_access.newsletter_subscription(email=email, subscription_status=False)

        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"] }
            
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success' : False, 'message' : get_error_message(e)}
    