import requests
from fastapi import APIRouter, Depends

from src.data_access.topup import crypto_deposit as data_access
from src.misc.constants.messages import (DATABASE_CONNECTION_ERROR, OK)
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.schemas.Topup import GetCryptoDeposit
from src.utilities.aes import aes
from src.utilities.utils import get_error_message, config, dataFrameToJsonObject

router = APIRouter()

crypto_payment_gateway_config = config['CryptoPaymentGateway']


@router.get('/get_deposit_currencies', dependencies=[Depends(RightsChecker([222]))])
async def get_deposit_currencies(token_payload: any = Depends(get_current_user)):
    try:
        response = requests.get(crypto_payment_gateway_config['BaseURL']+'get_deposit_currencies?api_key='+crypto_payment_gateway_config['AppKey'])

        data = response.json()

        print(data)
        if data['success']:
            return {'success': True, 'message': OK, 'data': data['data'] }

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_deposit_address', dependencies=[Depends(RightsChecker([222]))])
async def get_deposit_address(network: str, currency_symbol: str, currency_code: str, amount: float, token_payload: any = Depends(get_current_user)):
    try:
        url = crypto_payment_gateway_config['BaseURL']+'request_deposit_address?api_key='+crypto_payment_gateway_config['AppKey']+'&currency_code='+currency_code+'&payout_type=ASAP'
        response = requests.get(url)

        data = response.json()

        print(data)
        if data['success']:
            address = data['address']
            address_qr = data['address_qr']
            payment_request_id = data['deposit_request_id']

            dataset = data_access.save_crypto_deposit_request_details(user_id=token_payload['user_id'], network=network, token_symbol=currency_symbol, payment_request_id=payment_request_id, amount=amount)

            if len(dataset) > 0 and len(dataset['rs']) > 0:
                ds = dataset['rs']
                if ds.iloc[0].loc["success"]:
                    return {'success': True, 'message': OK, 'address': address, 'address_qr': address_qr, 'request_id': aes.encrypt(str(ds.iloc[0].loc["request_id"])), 'address_validity_seconds': data['address_validity_seconds']}

                return {'success': False, 'message': ds.iloc[0].loc["message"]}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/check_for_new_deposits')
def check_for_new_deposits():
    try:
        req = GetCryptoDeposit()
        req.input_txn_status='Pending'
        pending_dataset = data_access.get_crypto_deposits_history(req=req)
        
        deposit_request_ids = ''
        if len(pending_dataset) > 0 and len(pending_dataset['rs']) > 0:
            pending_requests = pending_dataset['rs']
            
            for i, dr in pending_requests.iterrows():
                if deposit_request_ids != '':
                    deposit_request_ids += ','
                    
                deposit_request_ids += dr['payment_request_id']
        
        response = requests.get(crypto_payment_gateway_config['BaseURL']+'get_deposit_details?api_key='+crypto_payment_gateway_config['AppKey']+'&deposit_request_ids='+deposit_request_ids)

        response = response.json()
        
        if response['success']:
            for data in response['data']:

                dataset = data_access.update_crypto_deposit_request_details(payment_request_id=str(data['deposit_request_id']),
                                                                            input_txn_hash=str(data['input_txn_hash']),
                                                                            input_txn_explorer_url=str(data['input_txn_hash_explorer_url']),
                                                                            in_amount=data['in_amount'],
                                                                            input_txn_status=str(data['input_txn_status']),
                                                                            input_txn_timestamp=int(data['input_txn_timestamp']),
                                                                            out_transaction_hash=str(data['out_transaction_hash']),
                                                                            output_txn_explorer_url=str(data['out_txn_hash_explorer_url']),
                                                                            out_transaction_status=str(data['out_transaction_status']),
                                                                            out_transaction_date=int(data['output_txn_timestamp']),
                                                                            out_amount=data['out_amount'],
                                                                            out_processing_fee=data['out_processing_fee'])

                # if len(dataset) > 0 and len(dataset['rs']) > 0:
                #     return {'success': True, 'message': 'Deposit details saved successfully! Payment Id: '+payment_request_id}

                # return {'success': False, 'message': 'Some error occurred while saving details!'}
            return {'success': True, 'message': 'Deposit details saved successfully!'}
        return {'success': False, 'message': 'No details found for the deposit!'}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}



@router.get('/crypto_deposit_callback')
def crypto_deposit_callback(payment_request_id: str):
    try:
        response = requests.get(crypto_payment_gateway_config['BaseURL']+'get_payment_details?app_key='+crypto_payment_gateway_config['AppKey']+'&payment_request_id='+payment_request_id)

        data = response.json()
        # print(data)
        if data['success']:
            data = data['data'][0]

            dataset = data_access.update_crypto_deposit_request_details(payment_request_id=payment_request_id,
                                                                        input_txn_hash=str(data['input_txn_hash']),
                                                                        input_txn_explorer_url=str(data['input_txn_hash_explorer_url']),
                                                                        in_amount=data['in_amount'],
                                                                        input_txn_status=str(data['input_txn_status']),
                                                                        input_txn_timestamp=int(data['input_txn_timestamp']),
                                                                        out_transaction_hash=str(data['out_transaction_hash']),
                                                                        output_txn_explorer_url=str(data['out_txn_hash_explorer_url']),
                                                                        out_transaction_status=str(data['out_transaction_status']),
                                                                        out_transaction_date=int(data['out_transaction_date']),
                                                                        out_amount=data['out_amount'],
                                                                        out_processing_fee=data['out_processing_fee'])

            if len(dataset) > 0 and len(dataset['rs']) > 0:
                return {'success': True, 'message': 'Deposit details saved successfully! Payment Id: '+payment_request_id}

            return {'success': False, 'message': 'Some error occurred while saving details!'}
        return {'success': False, 'message': 'No details found for the deposit!'}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}



# @router.get('/get_crypto_deposit_request_details', dependencies=[Depends(RightsChecker([222]))])
# async def get_crypto_deposit_request_details(request_id: str, token_payload: any = Depends(get_current_user)):
#     try:
#         request_id = int(aes.decrypt(request_id))
#         dataset = data_access.get_crypto_deposit_request_details(request_id=request_id)
#
#         if len(dataset) > 0 and len(dataset['rs']) > 0:
#             ds = dataset['rs']
#             if ds.iloc[0].loc['success']:
#                 return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(dataset['rs'])}
#             return {'success': False, 'message': 'Pending'}
#         return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
#
#     except Exception as e:
#         print(e.__str__())
#         return {'success': False, 'message': get_error_message(e)}


@router.post('/get_crypto_deposit_history', dependencies=[Depends(RightsChecker([222, 224]))])
def get_crypto_deposit_history(req: GetCryptoDeposit, token_payload: any = Depends(get_current_user)):
    try:
        match_exact_user_id = False
        if token_payload["role"] == 'User':
            req.user_id = token_payload["user_id"]
            match_exact_user_id = True

        if req.request_id != '' and req.request_id is not None:
            req.request_id = int(aes.decrypt(req.request_id))
        else:
            req.request_id = 0

        dataset = data_access.get_crypto_deposits_history(req=req, match_exact_user_id=match_exact_user_id)
        # print(dataset)
        if len(dataset) > 0:
            ds = dataset['rs']
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(ds),
                    'data_count': int(dataset['rs1'].iloc[0].loc["total_records"])}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
