
from fastapi import APIRouter
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR
from src.data_access.home import contact_us as data_access
from src.schemas.Home import ContactUs
from src.utilities.utils import get_error_message


router = APIRouter(
    prefix="/contact_us"
    )

@router.post('/save_message')
def save_message(req: ContactUs):
    try:
        dataset = data_access.save_message(name=req.name, email=req.email, type=req.type, subject=req.subject, message=req.message)

        if len(dataset)>0 and len(dataset['rs']):
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                return {'success': True, 'message': ds.iloc[0].loc["message"] }
            
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success' : False, 'message' : get_error_message(e)}
    
