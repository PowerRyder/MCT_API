
from src.misc.helpers.helper_utils import company_dict, get_sms_template, send_sms


def send_joining_sms(user_id, user_name, mobile_no):
    template_id, msg_temp = get_sms_template("joining_sms")

    a = {
            'user_id':user_id,
            'user_name':user_name
        }

    c = a | company_dict

    msg = msg_temp.format_map(c)
    
    return send_sms(mobile_no=mobile_no, message=msg, template_id=template_id)

def send_two_factor_auth_otp_sms(user_id, user_name, mobile_no, otp):
    template_id, msg_temp = get_sms_template("two_factor_auth_otp")

    a = {
            'user_id':user_id,
            'user_name':user_name,
            'otp':otp
        }

    c = a | company_dict

    msg = msg_temp.format_map(c)
    
    return send_sms(mobile_no=mobile_no, message=msg, template_id=template_id)

def send_reset_password_link_sms(user_id, user_name, mobile_no, reset_link):
    template_id, msg_temp = get_sms_template("password_reset_link")
    
    a = {
            'user_id':user_id,
            'user_name':user_name,
            'reset_link':reset_link
        }

    c = a | company_dict

    msg = msg_temp.format_map(c)
    
    return send_sms(mobile_no=mobile_no, message=msg, template_id=template_id)

def send_contact_verification_otp_sms(user_id, user_name, mobile_no, otp):
    template_id, msg_temp = get_sms_template("verification_otp")
   
    a = {
            'user_id':user_id,
            'user_name':user_name,
            'otp':otp
        }

    c = a | company_dict

    msg = msg_temp.format_map(c)

    return send_sms(mobile_no=mobile_no, message=msg, template_id=template_id)

def send_topup_sms(user_id, user_name, mobile_no, package_name):
    template_id, msg_temp = get_sms_template("topup_success")
   
    a = {
            'user_id':user_id,
            'user_name':user_name,
            'package_name':package_name
        }

    c = a | company_dict

    msg = msg_temp.format_map(c)

    return send_sms(mobile_no=mobile_no, message=msg, template_id=template_id)

def send_withdrawal_successful_sms(user_id, user_name, mobile_no, amount):
    template_id, msg_temp = get_sms_template("withdrawal_successful")
   
    a = {
            'user_id':user_id,
            'user_name':user_name,
            'amount':amount
        }

    c = a | company_dict

    msg = msg_temp.format_map(c)

    return send_sms(mobile_no=mobile_no, message=msg, template_id=template_id)

def send_withdrawal_rejected_sms(user_id, user_name, mobile_no, amount):
    template_id, msg_temp = get_sms_template("withdrawal_rejected")
   
    a = {
            'user_id':user_id,
            'user_name':user_name,
            'amount':amount
        }

    c = a | company_dict

    msg = msg_temp.format_map(c)

    return send_sms(mobile_no=mobile_no, message=msg, template_id=template_id)
