
from fastapi import APIRouter, Depends, Response
import pandas as pd
import pystache
import pdfkit
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.Topup import TopupDetailsRequest
from src.data_access.topup import topup as data_access
from src.utilities.utils import config, getPdfKitConfig, convert_timestamp_to_datetime_with_timezone
from src.misc.helpers.helper_utils import company_dict


router = APIRouter()

@router.get('/get_topup_receipt', dependencies=[Depends(RightsChecker([82, 83, 84]))])
def get_topup_receipt(pin_number: int):
    pdf_bytes = get_topup_receipt_pdf_bytes(pin_number=pin_number)
    response = Response(content=pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=sample.pdf"
    return response
    # return get_topup_receipt_html(pin_number)

def get_topup_receipt_pdf_bytes(pin_number: int):
    html = get_topup_receipt_html(pin_number=pin_number)
    config = getPdfKitConfig()
    pdf_bytes = pdfkit.from_string(html, False, configuration=config)
    return pdf_bytes


@router.get('/get_topup_receipt_html', dependencies=[Depends(RightsChecker([82, 83, 84]))])
def get_topup_receipt_html(pin_number: int):
    req =  TopupDetailsRequest(pin_number=pin_number)
    dataset = data_access.topup_details(req=req)
    # print(dataFrameToJsonObject(dataset['rs']))
    df = dataset['rs']
    row = df.iloc[0]
    with open('templates/docs/topup_receipt.html', 'r') as file:
        template = file.read()
        a = {
                'transaction_id': int(pd.Timestamp(row['topup_date']).timestamp())*2,
                'user_id':row['user_id'],
                'user_name':row['name'],
                'topup_date':convert_timestamp_to_datetime_with_timezone(row['topup_date']),
                'package':row['package'],
                'pin_value':round(row['pin_value'], int(company_dict['round_off_digits'])),
                'tax_percentage':round(row['tax_percentage'], int(company_dict['round_off_digits'])),
                'tax_amount':round(row['tax_amount'], int(company_dict['round_off_digits'])),
                'pin_value_with_tax':round(row['pin_value_with_tax'], int(company_dict['round_off_digits'])),
                'payment_mode':row['payment_mode'],
                
            }

        c = a | company_dict
        
        template = pystache.render(template, c)
                      
        return template
    