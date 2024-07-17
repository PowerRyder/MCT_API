from src.misc.helpers.helper_utils import company_dict, get_email_template, send_mail, send_mail_async
import pystache


def send_joining_mail(user_id, user_name, email_id, joining_amount, sponsor_id, referral_link, in_memory_files=None):
    template:str = get_email_template('registration')
    
    a = {
            'user_id':user_id,
            'user_name':user_name,
            'joining_amount':joining_amount,
            'sponsor_id':sponsor_id,
            'referral_link':referral_link
        }

    c = a | company_dict
    template = pystache.render(template, c)
    
    return send_mail(email_id, 'Welcome Mail', template, None, in_memory_files=in_memory_files)
            

def send_reset_password_link_mail(user_id, user_name, email_id, reset_link):
    template = get_email_template('reset_password')
    
    a = {
            'user_id':user_id,
            'user_name':user_name,
            'reset_link':reset_link
        }

    c = a | company_dict

    template = pystache.render(template, c)
                                
    return send_mail(email_id, 'Reset Password', template)

def send_contact_verification_otp_mail(user_id, user_name, email_id, otp):
    template = get_email_template('email_verification_otp')
    
    a = {
            'user_id':user_id,
            'user_name':user_name,
            'otp':otp
        }

    c = a | company_dict
      
    template = pystache.render(template, c)
                                
    return send_mail(email_id, 'OTP for Email Verification', template)

def send_email_verification_link_mail(user_id, user_name, verification_link, email_id):
    template = get_email_template('email_verification_link')
    
    a = {
            'user_id':user_id,
            'user_name':user_name,
            'verification_link':verification_link
        }

    c = a | company_dict
      
    template = pystache.render(template, c)
                                 
    return send_mail(email_id, 'Email Verification Link', template)

def send_two_factor_auth_otp_mail(user_id, user_name, email_id, otp):
    template = get_email_template('two_factor_auth_otp')
    
    a = {
            'user_id':user_id,
            'user_name':user_name,
            'otp':otp
        }

    c = a | company_dict
      
    template = pystache.render(template, c)
                                
    return send_mail(email_id, 'Two Factor Authentication OTP', template)

def send_topup_mail(user_id, user_name, email_id, package_name, pin_value, in_memory_files=None):
    template = get_email_template('topup_successful')
    
    a = {
            'user_id':user_id,
            'user_name':user_name,
            'package_name':package_name,
            'pin_value':pin_value
        }

    c = a | company_dict
      
    template = pystache.render(template, c)
                         
    return send_mail(email_id, 'Topup Successful', template, None, in_memory_files=in_memory_files)


def send_withdrawal_successful_mail(user_id, user_name, email_id, amount):
    template = get_email_template('withdrawal_successful')
    
    a = {
            'user_id':user_id,
            'user_name':user_name,
            'amount':amount
        }

    c = a | company_dict
      
    template = pystache.render(template, c)
                                
    return send_mail_async(email_id, 'Withdrawal Successful', template)

def send_withdrawal_rejected_mail(user_id, user_name, email_id, amount):
    template = get_email_template('withdrawal_rejected')
    
    a = {
            'user_id':user_id,
            'user_name':user_name,
            'amount':amount
        }

    c = a | company_dict
      
    template = pystache.render(template, c)
                                
    return send_mail_async(email_id, 'Withdrawal Rejected', template)
