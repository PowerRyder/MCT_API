
from fastapi import APIRouter, Depends, Response
import pdfkit
import pystache
from src.data_access.user import details as user_details_data_access
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.utilities.utils import config, get_error_message, getPdfKitConfig, convert_timestamp_to_datetime_with_timezone
from src.misc.helpers.helper_utils import company_dict


router = APIRouter(dependencies=[Depends(get_current_user)])
 
@router.get('/get_welcome_letter', dependencies=[Depends(RightsChecker([116]))])
def get_welcome_letter(user_id: str):
    try:
        pdf_bytes = get_welcome_letter_pdf_bytes(user_id=user_id)
        response = Response(content=pdf_bytes)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=welcome.pdf"
        return response
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
    

@router.get('/get_welcome_letter_html', dependencies=[Depends(RightsChecker([116]))])
def get_welcome_letter_html(user_id: str):
    try:
        dataset = user_details_data_access.get_user_details(user_id=user_id)
        # print(dataFrameToJsonObject(dataset['rs']))
        df = dataset['rs']
        row = df.iloc[0]
        with open('templates/docs/welcome_letter.html', 'r') as file:
            template = file.read()
            a = {
                    'user_id':row['user_id'],
                    'user_name':row['name'],
                    'joining_date':convert_timestamp_to_datetime_with_timezone(row['joining_date']),
                    'sponsor_id':row['sponsor_id'],
                    'joining_amount':round(row['joining_amount'], int(company_dict['round_off_digits']))
                }

            c = a | company_dict

            template = pystache.render(template, c)

            return template

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


def get_welcome_letter_pdf_bytes(user_id: str):
    html = get_welcome_letter_html(user_id=user_id)
    config = getPdfKitConfig()
    pdf_bytes = pdfkit.from_string(html, False, configuration=config)
    return pdf_bytes

