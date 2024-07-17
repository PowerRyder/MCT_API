
from fastapi import APIRouter, Request
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.utilities.utils import get_error_message, get_ip_info, company_details, config
from src.data_access.home import visitors as data_access

router = APIRouter()

@router.get('/')
def visited(request: Request):
    try:
        url = dict(request.scope["headers"]).get(b"referer", b"").decode() # request.base_url.__str__()
        
        if(request.client is None):
            client_ip_address = request.headers['x-forwarded-for']
        else:
            client_ip_address = request.client.host

        ip_details = None
        if(not config['IsDevelopment']):
            ip_details = get_ip_info(client_ip_address)

        dataset = data_access.save_visitor(url=url, ip_address=client_ip_address, ip_details=ip_details)

        if len(dataset) > 0:

            login_info_df = dataset['rs']

            if len(login_info_df) > 0:
                return {'success': True, 'message': 'Welcome to '+company_details['name']+' API'}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success' : False, 'message' : get_error_message(e)}
    