
import asyncio
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import glob
import json
import os
# import smtplib
import aiosmtplib
import pandas as pd
import requests
from src.utilities.utils import company_details, config
from datetime import date
from requests.auth import HTTPBasicAuth
from src.data_access import misc as misc_data_access


def get_company_details_dict():
    todays_date = date.today()
    # print(company_details)
    return {
            'company_name':company_details.loc["name"], 
            'company_address':company_details.loc["address"],
            'logo':company_details.loc["logo"],
            'website_url':company_details.loc["website"],
            'year':todays_date.year,
            'otp_validity_minutes':company_details.loc["otp_validity_minutes"],
            'currency_symbol':company_details.loc["currency_symbol"],
            'is_currency_symbol_prefixed':company_details.loc["is_currency_symbol_prefixed"],
            'tax_name':company_details.loc["tax_name"],
            'round_off_digits':company_details.loc["round_off_digits"]
            }
         
company_dict = get_company_details_dict()
   
def compile_email_formats_mjml():
    delete_precompiled_templates()

    try:
        dir_list = os.listdir('templates/email/mjml/')
        for file_name_with_extension in dir_list:
            if file_name_with_extension.endswith(".mjml"):
                split_tup = os.path.splitext(file_name_with_extension)
                
                file_name = split_tup[0]
                
                with open('templates/email/mjml/'+file_name_with_extension, 'r') as file:
                    template = file.read()

                result = requests.post(url='https://api.mjml.io/v1/render', auth=HTTPBasicAuth(config["mjml"]["AppId"], config["mjml"]["SecretKey"]),
                json={"mjml":template})

                json.loads(result.text)['html']

                with open('templates/email/compiled/'+file_name+'.html', 'a') as file:
                    file.write(json.loads(result.text)['html'])
    except Exception as e:
        print(e.__str__())


def delete_precompiled_templates():
    try:
        files = glob.glob('templates/email/compiled/*.html')
        for f in files:
            os.remove(f)
    except Exception as e:
        print(e.__str__())


def get_email_template(template_name):
    with open('templates/email/compiled/'+template_name+'.html', 'r') as file:
        template = file.read()
        # print(template)
        return template


def get_sms_template(template_name):
    d = pd.read_csv('templates/sms_templates.csv', delimiter=';', dtype = str)
    # print(d)
    d.set_index('template_name', inplace=True)
    template_id = d.loc[template_name][0]
    msg_template:str = d.loc[template_name][1]
    return template_id, msg_template

def send_sms(mobile_no, message, template_id):
    print(message)
    is_sms_system = bool(company_details.loc["is_sms_configured"])
    
    if(is_sms_system):
        if(mobile_no is not None):
            smsUser = config["SMS"]["User"]
            smsPassword = config["SMS"]["Password"]
            smsSenderId = config["SMS"]["SenderId"]
            
            SMSURL = f"""http://whybulksms.in/app/smsapi/index.php?username={smsUser}
            &password={smsPassword}&campaign=10525&routeid=6&type=text&contacts={mobile_no}
            &senderid={smsSenderId}&msg={message}&template_id={template_id}"""
            
            # response = requests.get(SMSURL)
            
            d = "" #response.text
            
            if(d.find('NOT') == -1):
                return True, "SMS sent successfully!"
            return False, "Failed to send SMS!"
        return False, "Receiver mobile number not found!"
            
    return False, "SMS system not supported!"
  
  
# bulk email sending takes time, to send email asynchronously and use that async method as normal method for single mail.
def send_mail(recipients, subject, mailBody, attachments=None, in_memory_files=None):
    return asyncio.run(send_mail_async(recipients=recipients, subject=subject, mailBody=mailBody, attachments=attachments, in_memory_files=in_memory_files))
    
async def send_mail_async(recipients, subject, mailBody, attachments=None, in_memory_files=None):
    """
    Send an email asynchronously, with or without attachments.

    :param from_email: Sender email address.
    :param from_password: Sender email password.
    :param to_email: Receiver email address.
    :param subject: Email subject.
    :param body: Email body content.
    :param attachments: List of file paths to attach, default is None.
    :param in_memory_files: List of tuples where each tuple is (filename, bytes), default is None.
    """
    
    is_email_system = company_details.loc["is_email_configured"]
    
    if(is_email_system):
        if(recipients is not None and recipients!=""):
            try:
                emailUser = config["EMAIL"]["User"]
                emailPassword = config["EMAIL"]["AppPassword"]
                emailHostAddress = config["EMAIL"]["HostAddress"]
                emailServerPort = config["EMAIL"]["Port"]
                
                recipients = recipients if isinstance(recipients, list) else [recipients]
            
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = emailUser
                msg['To'] = ", ".join(recipients)

                part = MIMEText(mailBody, 'html')
                msg.attach(part)
            
                # Attach files from file paths if provided
                if attachments:
                    for file_path in attachments:
                        with open(file_path, 'rb') as attachment_file:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment_file.read())
                            encoders.encode_base64(part)
                            part.add_header('Content-Disposition', f"attachment; filename= {file_path.split('/')[-1]}")
                            msg.attach(part)

                # Attach in-memory files if provided
                if in_memory_files:
                    for filename, file_bytes in in_memory_files:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(file_bytes)
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
                        msg.attach(part)

                server = aiosmtplib.SMTP(hostname=emailHostAddress, port=emailServerPort)
                await server.connect()
                # await server.starttls()
                # await server.ehlo()
                await server.login(emailUser, emailPassword)
                await server.send_message(sender=emailUser, recipients=recipients, message=msg)
                await server.quit()
                print("Email sent successfully!")
                return True, "Email sent successfully!"
                
            except aiosmtplib.SMTPException as e:
                print("Error: unable to send email", e)

            print("Unable to send email!")
            return False, "Unable to send email"

        print("Receiver email not found!")
        return False, "Receiver email not found!"

    print("Email system not supported!")
    return False, "Email system not supported!"


def generate_routes_json():
    if(config["IsDevelopment"]):
        dataset = misc_data_access.get_all_routes()

        if len(dataset) > 0:
            df = dataset['rs']

            if len(df) > 0:
                d = df.to_dict(orient='records')

                mod_d = dict({})
                for obj in d:
                    mod_d[obj['control_id']] = obj

                mod_d = json.dumps(mod_d)

                file_path = config["AppRoutesJsonFilePath"]
                if os.path.exists(file_path):
                    os.remove(file_path)

                with open(file_path, 'a') as file:
                    file.write(mod_d)
    

                file_path = config["ApiRoutesJsonFilePath"]
                if os.path.exists(file_path):
                    os.remove(file_path)

                with open(file_path, 'a') as file:
                    file.write(mod_d)
    

def get_route_by_control_id(control_id: str):
    file_path = config["ApiRoutesJsonFilePath"]
    with open(file_path, 'r') as file:
        routes = json.load(file)
        return routes[control_id]