
from fastapi import APIRouter, Depends, Response
import pandas as pd
import pystache
import pdfkit
from src.data_access.user import details as user_details_data_access
from src.misc.security.RightsChecker import RightsChecker
from src.utilities.utils import config, getPdfKitConfig
from src.misc.helpers.helper_utils import company_dict, company_details


router = APIRouter()

@router.get('/get_user_id_card', dependencies=[Depends(RightsChecker([117]))])
def get_user_id_card(user_id: str):
    pdf_bytes = get_user_id_card_pdf_bytes(user_id=user_id)
    response = Response(content=pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=sample.pdf"
    return response


def get_user_id_card_pdf_bytes(user_id: str):
    html = get_user_id_card_html(user_id=user_id)
    config = getPdfKitConfig()
    pdf_bytes = pdfkit.from_string(html, False, configuration=config)
    return pdf_bytes


@router.get('/get_user_id_card_html', dependencies=[Depends(RightsChecker([117]))])
def get_user_id_card_html(user_id: str):
    dataset = dataset = user_details_data_access.get_user_details(user_id=user_id)
    # print(dataFrameToJsonObject(dataset['rs']))
    df = dataset['rs']
    row = df.iloc[0]
    with open('templates/docs/id_card.html', 'r') as file:
        template = file.read()
        a = {
                'user_id':row['user_id'],
                'user_name':row['name'],
                'joining_date':row['joining_date'].strftime(config['DateTimeLongFormat']),
                'designation':'Member',
                'photo':company_details['api_base_url']+'static/images/profile/'+row['profile_image_url']
            }

        c = a | company_dict
        
        template = pystache.render(template, c)
                      
        return template
    
