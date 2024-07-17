import base64
import json
import os

import ipinfo
import magic
import pandas as pd
import pdfkit
import psycopg2
import pyotp
from mimetypes import guess_extension
from datetime import datetime

from src.misc.constants.messages import UNKNOWN_ERROR

with open("config.json") as json_data_file:
    config = json.load(json_data_file)
    
    conn_string = config["ConnectionString"]


def execute_query(query, params=None) -> dict[str, pd.DataFrame]:
    conn = psycopg2.connect(conn_string)

    result = {}
    try:
        cur = conn.cursor()
        cur.execute(query, params)

        cursor_names = cur.fetchall()
        
        if len(cursor_names)>0:
                
            cursor_names = cursor_names[0]
            
            for _cursor in cursor_names:
                try:
                        
                    cur.execute(f'fetch all in {_cursor}')
                    d = cur.fetchall()
                    df = pd.DataFrame(d, columns=[i[0] for i in cur.description])
                    
                    result[_cursor] = df
                except Exception as e:
                    pass
        else:
            pass
        
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    
    return result


company_datasets = execute_query("call usp_get_company_details()")
company_details = company_datasets['rs'].iloc[0]


def reload_company_details():
    global company_datasets
    global company_details
    company_datasets = execute_query("call usp_get_company_details()")
    company_details = company_datasets['rs'].iloc[0]
    

def dataFrameToJsonObject(df: pd.DataFrame):
    # print(df.columns)
    jsonStr = df.to_json(orient='records')
    jsonObj = json.loads(jsonStr)
    return jsonObj


def toJsonObj(obj):
        return json.loads(json.dumps(obj, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))


def get_error_message(e):
    if e is not None:
        execute_query("call usp_save_api_error_log(_error_msg => %s)", (e.__str__(), ))
        if config['IsDevelopment']:
            return 'Error : '+e.__str__()

    return UNKNOWN_ERROR


def hide_mobile_no(mobile_no):
    return (mobile_no[0:2]+'X'*(len(mobile_no)-5)) + mobile_no[len(mobile_no)-3:]


def hide_email_address(email_id):
    return (email_id[0:2]+'X'*(len(email_id.split('@')[0])-4)) + email_id[len(email_id)-(3+len(email_id.split('@')[1])):]


def is_valid_google_authenticator_code(key:str, code:str):
    totp = pyotp.TOTP(key)
    return totp.verify(code)


def generate_google_authenticator_secret_key():
    return pyotp.random_base32()


def get_ip_info(ip_address: str):
    handler = ipinfo.getHandler(config["IP_Info_Key"])
    details = handler.getDetails(ip_address)

    details = json.dumps(details.details)
    return details


def intersection(lst1, lst2):
    return set(lst1).intersection(lst2)


def addCurrencySymbol(amount):
    return company_details['currency_symbol']+str(amount) if company_details['is_currency_symbol_prefixed'] else str(amount)+' '+company_details['currency_symbol']


def getPdfKitConfig():
    if(not config['IsDevelopment']):
        return pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    return None


def convert_timestamp_to_datetime_with_timezone(input_value):
    """
    Convert a Pandas timestamp or numeric timestamp to a datetime string with a specified timezone.

    Args:
        input_value: Input timestamp, which can be a Pandas timestamp or a numeric timestamp.
        desired_timezone: The desired timezone for the output string.

    Returns:
        A formatted datetime string with the specified timezone.
    """

    desired_timezone = config["TimeZone"]
    if isinstance(input_value, (pd.Timestamp, pd.DatetimeIndex)):
        # If input is a Pandas timestamp, convert it to the desired timezone
        timestamp_with_timezone = input_value.tz_convert(desired_timezone)
    elif isinstance(input_value, (int, float)):
        # If input is a numeric timestamp, convert it to a Pandas timestamp
        timestamp_with_timezone = pd.Timestamp.fromtimestamp(input_value, tz=desired_timezone)
    else:
        raise ValueError(
            "Input value must be a Pandas timestamp, numeric timestamp (seconds since epoch), or a Pandas DatetimeIndex.")

        # Format the timestamp as a datetime string with the specified timezone
    formatted_datetime = timestamp_with_timezone.strftime(config["DateTimeLongFormat"])

    return formatted_datetime


def save_base64_file(data, upload_file_name='Upload', output_directory="static/images/uploads"):
    """
    Decode the base64 string, identify the file extension, and save the file to disk.

    Parameters:
    - data: base64 encoded string.
    - upload_purpose: Purpose to upload the file, it is used in file name while saving
    - output_directory: The directory where the file will be saved.

    Returns:
    - The path of the saved file.
    """

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if data.startswith("data:"):
        data = data.split(",")[-1]

    # Decode the base64 data
    decoded_data = base64.b64decode(data)

    # Identify the file extension using magic library
    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(decoded_data)
    extension = guess_extension(mime_type)

    if extension in ['.png', '.jpg', '.jpeg']:

        filename = upload_file_name+'_'+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+extension

        file_path = os.path.join(output_directory, filename)

        # Save the file
        with open(file_path, 'wb') as f:
            f.write(decoded_data)

        return filename, file_path
    else:
        raise ValueError("Invalid file type!")
