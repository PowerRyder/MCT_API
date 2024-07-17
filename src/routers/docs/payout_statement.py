import pandas as pd
import pdfkit
import pystache
from fastapi import APIRouter, Depends, Response

from src.data_access.income import total as data_access
from src.misc.helpers.helper_utils import company_dict
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.Income import GetTotalIncome_Request
from src.utilities.utils import config, getPdfKitConfig, convert_timestamp_to_datetime_with_timezone, company_details, \
    company_datasets, dataFrameToJsonObject

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get('/get_payout_statement', dependencies=[Depends(RightsChecker([170, 171]))])
def get_payout_statement(user_id: str, payout_no: int, wallet_id: int):
    pdf_bytes = get_payout_statement_pdf_bytes(user_id=user_id, payout_no=payout_no, wallet_id=wallet_id)
    response = Response(content=pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=sample.pdf"
    return response
    # return get_topup_receipt_html(pin_number)


def get_payout_statement_pdf_bytes(user_id: str, payout_no: int, wallet_id: int):
    html = get_payout_statement_html(user_id=user_id, payout_no=payout_no, wallet_id=wallet_id)
    config = getPdfKitConfig()
    pdf_bytes = pdfkit.from_string(html, False, configuration=config)
    return pdf_bytes


@router.get('/get_payout_statement_html', dependencies=[Depends(RightsChecker([170, 171]))])
def get_payout_statement_html(user_id: str, payout_no: int, wallet_id: int, token_payload: any = Depends(get_current_user)):
    # print("In function", token_payload)
    req = GetTotalIncome_Request(user_id=user_id, payout_no=payout_no, wallet_id=wallet_id)
    dataset = data_access.get_total_income(req=req, match_exact_user_id=True)

    df = dataset['rs']
    row = df.iloc[0]
    # print(row)
    with open('templates/docs/payout_statement.html', 'r') as file:
        template = file.read()

        income_rows = ''

        income_rows_format = '''
                            <tr>
                                <td class="doc-td">{}</td>
                                <td class="doc-td-2">{}</td>
                            </tr>
                            '''

        df = company_datasets["rs3"]

        for i, income_types_row in df.iterrows():
            # print(income_row)
            display_name = income_types_row["display_name"]
            total_income_column_name = income_types_row["total_income_column_name"]
            income_rows += income_rows_format.format(display_name, round(row[total_income_column_name], int(company_dict['round_off_digits'])))

        deduction_rows = ''
        deduction_rows_format = '''
                                <div class="doc-total-row">
                                    <span class="doc-total-label">{}</span>
                                    <span class="doc-total-amount">{}</span>
                                </div>
                                '''

        deduction_rows += deduction_rows_format.format('Total Income', round(row["total_income"], int(company_dict['round_off_digits'])))
        if(company_details['is_pair_deduction'] or company_details['is_matrix_deduction']):
            deduction_rows += deduction_rows_format.format('Deduction', round(row["total_deduction"], int(company_dict['round_off_digits'])))

        if(company_details['tds']>0):
            deduction_rows += deduction_rows_format.format('Tds', round(row["tds"], int(company_dict['round_off_digits'])))

        if (company_details['service'] > 0):
            deduction_rows += deduction_rows_format.format('Service', round(row["service"], int(company_dict['round_off_digits'])))

        if (company_details['repurchase'] > 0):
            deduction_rows += deduction_rows_format.format('Repurchase', round(row["repurchase"], int(company_dict['round_off_digits'])))

        if (company_details['other'] > 0):
            deduction_rows += deduction_rows_format.format('Other deduction', round(row["other"], int(company_dict['round_off_digits'])))

        deduction_rows += deduction_rows_format.format('Net Payable Income', round(row["net_income"], int(company_dict['round_off_digits'])))


        template = template.replace('{{income_rows}}', income_rows)
        template = template.replace('{{deduction_rows}}', deduction_rows)

        a = {
            'statement_id': int(pd.Timestamp(row['to_date']).timestamp()) * 2,
            'user_id': row['user_id'],
            'user_name': row['user_name'],
            'statement_period':convert_timestamp_to_datetime_with_timezone(row['from_date']) + ' To ' + convert_timestamp_to_datetime_with_timezone(row['to_date']),
            'total_income': round(row['total_income'], int(company_dict['round_off_digits'])),
            'deduction': round(row['total_deduction'], int(company_dict['round_off_digits'])),
            'tds': round(row['tds'], int(company_dict['round_off_digits'])),
            'service': round(row['service'], int(company_dict['round_off_digits'])),
            'repurchase': round(row['repurchase'], int(company_dict['round_off_digits'])),
            'other': round(row['other'], int(company_dict['round_off_digits'])),
            'net_income': round(row['net_income'], int(company_dict['round_off_digits']))
        }

        c = a | company_dict

        template = pystache.render(template, c)

        return template
