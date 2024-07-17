
import asyncio
import json
import time

import requests
from fastapi import APIRouter, Depends
from src.misc.helpers.email_helper import send_withdrawal_rejected_mail, send_withdrawal_successful_mail
from src.misc.helpers.sms_helper import send_withdrawal_rejected_sms, send_withdrawal_successful_sms
from src.misc.security.RightsChecker import RightsChecker
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.data_access.withdrawal import withdrawal as data_access

from src.misc.security.Jwt import get_current_user
from src.routers.withdrawal.crypto_withdrawal import send_token_on_binance
from src.schemas.Withdrawal import GetWithdrawalRequests, WithdrawFund, WithdrawalRequestApproveRejectDataItem
from src.utilities.aes import aes
from src.utilities.utils import addCurrencySymbol, dataFrameToJsonObject, get_error_message, config

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

crypto_payment_gateway_config = config['CryptoPaymentGateway']

@router.post('/withdraw_fund', dependencies=[Depends(RightsChecker([110, 111]))])
async def withdraw_fund(req: WithdrawFund, token_payload:any = Depends(get_current_user)):
    try:

        if req.two_factor_auth_request_id != '':
            req.two_factor_auth_request_id = int(aes.decrypt(req.two_factor_auth_request_id))
        else:
            req.two_factor_auth_request_id = 0
            
        user_id = token_payload["user_id"]
        user_type = token_payload["role"]

        dataset = data_access.withdraw_fund(req=req, user_id=user_id, user_type=user_type)
        if len(dataset) > 0 and len(dataset['rs']):
            dr = dataset['rs'].iloc[0]
            
            if dr.loc["success"]:
                # data = send_token_on_binance(private_key=config['PvKey'], to_address=req.crypto_wallet_address, amount=dr.loc["amount_withdrawn"], token_contract_address="0x55d398326f99059fF775485246999027B3197955", decimals=18)
                # # data = {
                # #     "app_key": crypto_payment_gateway_config['AppKey'],
                # #     "network": req.crypto_network,
                # #     "currency_symbol": req.token_symbol,
                # #     "to_address": req.crypto_wallet_address,
                # #     "amount": float(dr.loc["amount_withdrawn"]),
                # #     'reference_no': int(dr.loc["gateway_reference_no"])
                # # }
                # #
                # # headers = {
                # #     'Content-Type': 'application/json'
                # # }
                # #
                # # response = requests.post(crypto_payment_gateway_config['BaseURL'] + 'request_withdrawal', data=json.dumps(data), headers=headers)
                # # data = response.json()
                # # print(data)
                # if data['success']:
                #     d = data['data']
                #     if d['success_status']:
                #         data_access.update_withdrawal_requests_status_crypto(reference_no_for_gateway=int(dr['gateway_reference_no']), status='Approved', remarks=data['message'], txn_hash=d['transaction_hash'])
                #         return {'success': True, 'message': 'Withdrawal Successful!'}

                #     data_access.update_withdrawal_requests_status_crypto(reference_no_for_gateway=int(dr['gateway_reference_no']), status='Rejected', remarks=data['message'], txn_hash=d['transaction_hash'])
                #     return {'success': False, 'message': 'Withdrawal failed!'}

                # data_access.update_withdrawal_requests_status_crypto(reference_no_for_gateway=int(dr['gateway_reference_no']), status='Rejected', remarks=data['message'], txn_hash='')
                # return {'success': False, 'message': 'Withdrawal failed!'}

                return {'success': True, 'message': dr.loc["message"]}

            return {'success': False, 'message': dr.loc["message"]}

        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/withdraw_principle', dependencies=[Depends(RightsChecker([110, 111]))])
async def withdraw_principle(pin_srno: int, address: str, remarks: str = '', two_factor_auth_request_id: str = '', token_payload: any = Depends(get_current_user)):
    try:

        if two_factor_auth_request_id != '':
            two_factor_auth_request_id = int(aes.decrypt(two_factor_auth_request_id))
        else:
            two_factor_auth_request_id = 0

        user_id = token_payload["user_id"]

        dataset = data_access.withdraw_principle(user_id=user_id, pin_srno=pin_srno, address=address, remarks=remarks, two_factor_auth_request_id=two_factor_auth_request_id)
        if len(dataset) > 0 and len(dataset['rs']):
            dr = dataset['rs'].iloc[0]

            if dr.loc["success"]:
                data = send_token_on_binance(private_key=config['PvKey'], to_address=address,
                                             amount=dr.loc["amount_withdrawn"],
                                             token_contract_address="0x55d398326f99059fF775485246999027B3197955",
                                             decimals=18)

                if data['success']:
                    d = data['data']
                    if d['success_status']:
                        data_access.update_withdrawal_requests_status_principle(
                            pin_srno=pin_srno, status='Approved', txn_hash=d['transaction_hash'])
                        return {'success': True, 'message': 'Withdrawal Successful!'}

                    data_access.update_withdrawal_requests_status_principle(
                        pin_srno=pin_srno, status='Rejected', txn_hash=d['transaction_hash'])
                    return {'success': False, 'message': 'Withdrawal failed!'}

                data_access.update_withdrawal_requests_status_principle(
                    pin_srno=pin_srno, status='Rejected', txn_hash='')
                return {'success': False, 'message': 'Withdrawal failed!'}

                return {'success': True, 'message': dr.loc["message"]}

            return {'success': False, 'message': dr.loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.post('/get_withdrawal_requests', dependencies=[Depends(RightsChecker([112, 113, 114]))])
async def get_withdrawal_requests(req: GetWithdrawalRequests, token_payload:any = Depends(get_current_user)):
    try:
        match_exact_user_id=False

        if(token_payload["role"]!='Admin'):
            req.user_id = token_payload["user_id"]
            req.user_type = token_payload["role"]
            match_exact_user_id = True

        dataset = data_access.get_withdrawal_requests(req=req, match_exact_user_id=match_exact_user_id)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds), 'data_count': int(dataset['rs1'].iloc[0].loc["total_records"]) }
            
        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
    
    
@router.put('/update_withdrawal_requests_status', dependencies=[Depends(RightsChecker([113]))])
async def update_withdrawal_requests_status(dataItems:list[WithdrawalRequestApproveRejectDataItem], token_payload:any = Depends(get_current_user)):
    try:
        # start_time = time.time()
        user_id = token_payload["user_id"]
        
        data_dicts = json.dumps([item.dict() for item in dataItems])
        # print(data_dicts)
        dataset = data_access.update_withdrawal_requests_status(by_user_id=user_id, data_dicts=data_dicts, enable_lock_only=True)
        if len(dataset)>0:
            ds = dataset['rs']
            if(ds.iloc[0].loc["success"]):
                
                ds_user_details = dataset['rs1']
                tasks = []
                for index, row in ds_user_details.iterrows():
                    amount = addCurrencySymbol(row.loc["amount"])
                    if row.loc["status"] == "Approved":
                        
                        data = send_token_on_binance(private_key=config['PvKey'], to_address=row.loc['wallet_address'], amount=row.loc["amount"], token_contract_address="0x55d398326f99059fF775485246999027B3197955", decimals=18)

                        if data['success']:
                            d = data['data']
                            if d['success_status']:
                                data_access.update_withdrawal_requests_status_crypto(request_id=int(row.loc['request_id']), status='Approved', remarks='', txn_hash=d['transaction_hash'])
                                send_withdrawal_successful_sms(row.loc["user_id"], row.loc["user_name"], row.loc["mobile_no"], amount)
                                
                                tasks.append(send_withdrawal_successful_mail(row.loc["user_id"], row.loc["user_name"], row.loc["email_id"], amount ))
                                # return {'success': True, 'message': 'Withdrawal Successful!'}

                        
                    else:
                        send_withdrawal_rejected_sms(row.loc["user_id"], row.loc["user_name"], row.loc["mobile_no"], amount)
                        
                        tasks.append(send_withdrawal_rejected_mail(row.loc["user_id"], row.loc["user_name"], row.loc["email_id"], amount ))
                        
                await asyncio.gather(*tasks)
                
                data_access.unlock_withdrawal(data_dicts=data_dicts)
                # end_time = time.time()
                # print("--- %s seconds ---" % (end_time - start_time))
                return {
                        'success': True, 
                        'message': ds.iloc[0].loc["message"], 
                        'approved_count': int(ds.iloc[0].loc["approved_count"]),
                        'rejected_count': int(ds.iloc[0].loc["rejected_count"])
                        }
            
            return {'success': False, 'message': ds.iloc[0].loc["message"] }
        
        return {'success' : False, 'message' : DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        msg = get_error_message(e)
        data_access.unlock_withdrawal(data_dicts=data_dicts)
        
        return {'success': False, 'message': msg}
    
