
import pandas as pd
import pdfkit
from src.misc.helpers.email_helper import send_topup_mail
from src.misc.helpers.sms_helper import send_topup_sms
from src.routers.docs.topup_receipt import get_topup_receipt_html, get_topup_receipt_pdf_bytes
from src.utilities.utils import addCurrencySymbol


def send_topup_mail_and_sms(ds: pd.DataFrame):

    amount = addCurrencySymbol(ds.iloc[0].loc["pin_value"])
    pdf_bytes = get_topup_receipt_pdf_bytes(ds.iloc[0].loc["pin_number"])
    
    # pdf_bytes = pdfkit.from_string(textHtml, False)
    
    send_topup_sms(ds.iloc[0].loc["user_id"], ds.iloc[0].loc["user_name"], ds.iloc[0].loc["mobile_no"], ds.iloc[0].loc["package_name"])
    
    send_topup_mail(ds.iloc[0].loc["user_id"], ds.iloc[0].loc["user_name"], ds.iloc[0].loc["email_id"], ds.iloc[0].loc["package_name"], amount, [('Receipt.pdf', pdf_bytes)] )
    
    