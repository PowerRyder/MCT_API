import json
import time

import requests
from fastapi import APIRouter, Depends
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, INVALID_IFSC, OK
from src.data_access import misc as data_access
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.utilities.utils import dataFrameToJsonObject, get_error_message, config
from src.misc.constants import VALIDATORS
import pyqrcode


router = APIRouter(
    prefix="/misc",
    tags=["Miscellaneous"]
)


@router.get('/get_countries')
def get_countries():
    try:
        dataset = data_access.get_countries()

        if len(dataset) > 0:
            df = dataset['rs']

            if len(df) > 0:
                df = dataFrameToJsonObject(df)
                return {'success': True, 'message': OK, 'data': df }
                
            return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_states_by_country_id')
def get_states_by_country_id(country_id:int):
    try:
        dataset = data_access.get_states_by_country_id(country_id=country_id)
        # print(dataset)
        if len(dataset) > 0:
            df = dataset['rs']

            if len(df) > 0:
                df = dataFrameToJsonObject(df)
                return {'success': True, 'message': OK, 'data': df }
                
            return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_bank_details_by_ifsc')
def get_bank_details_by_ifsc(ifsc:str = VALIDATORS.IFSCODE):
    try:
        dataset = data_access.get_bank_details_by_ifsc(ifsc=ifsc)
        # print(dataset)
        if len(dataset) > 0:
            df = dataset['rs']

            if len(df) > 0:
                df = dataFrameToJsonObject(df)
                return {'success': True, 'message': OK, 'data': df }
                
            return {'success': False, 'message': INVALID_IFSC, 'data': [] }
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_supported_cryptos')
def get_supported_cryptos(action: str=VALIDATORS.CRYPTO_ACTION, id: int=0):
    try:
        dataset = data_access.get_supported_cryptos(action=action, id=id)
        # print(dataset)
        if len(dataset) > 0:
            df = dataset['rs']

            if len(df) > 0:
                df = dataFrameToJsonObject(df)
                return {'success': True, 'message': OK, 'data': df }
                
            return {'success': False, 'message': INVALID_IFSC, 'data': [] }
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_qr')
def get_qr(value:str):
    try:
        qr = pyqrcode.create(value)
        # print(dataset)
        return {'success': True, 'message': OK, 'qr': "data:image/png;base64,"+qr.png_as_base64_str(scale=5) }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/get_column_details')
def get_column_details(report_name: str):
    try:
        dataset = data_access.get_column_details(report_name=report_name)
        # print(dataset)
        if len(dataset) > 0:
            df = dataset['rs']

            if len(df) > 0:
                df = dataFrameToJsonObject(df)
                return {'success': True, 'message': OK, 'data': df }
                
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/filter_user_ids', dependencies=[Depends(RightsChecker([104]))])
def filter_user_ids(filter_value: str, user_type: str = VALIDATORS.USER_TYPE, token_payload:any = Depends(get_current_user)):
    try:
        
        # start_time = time.time()
        if(token_payload['role'] == 'User'):
            user_type = 'User'

        dataset = data_access.filter_user_ids(filter_value=filter_value, user_type=user_type)
        # print(dataset)
        if len(dataset) > 0:
            df = dataset['rs']
            # end_time = time.time()
            # print("--- %s seconds ---" % (end_time - start_time))
            return {'success': True, 'message': OK, 'data': dataFrameToJsonObject(df) }
                
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.get('/fetch_rates')
def fetch_rates():
    try:
        response = requests.get('https://min-api.cryptocompare.com/data/pricemulti?fsyms=USD,EUR,JPY,GBP,CNY,AUD,CAD,'
                                'CHF,HKD,NZD,INR,MXN,THB,ILS,IDR,CZK,AED,MYR,COP,RUB,RON,PEN,BHD,BGN,XAU'
                                '&tsyms=USD,EUR,JPY,GBP,CNY,AUD,CAD,CHF,HKD,NZD,INR,MXN,THB,ILS,IDR,CZK,AED,MYR,'
                                'COP,RUB,RON,PEN,BHD,BGN,XAU'
                                '&api_key='+config['CryptoCompareApiKey'])

        forex_data = response.json()

        response = requests.get('https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH,BNB,XRP,ADA,SOL,DOT,'
                                'DOGE,SHIB,LTC,UNI,LINK,MATIC,XLM,VET,TRX,BCH,ALGO,AXS,AAVE,USDT,AVAX,FTM&tsyms=BTC,ETH,BNB,XRP,'
                                'ADA,SOL,DOT,DOGE,SHIB,LTC,UNI,LINK,MATIC,XLM,VET,TRX,BCH,ALGO,AXS,AAVE,USDT,AVAX,FTM'
                                '&api_key='+config['CryptoCompareApiKey'])

        crypto_data = response.json()

        dataset = data_access.save_rates(forex_rates=json.dumps(forex_data), crypto_rates=json.dumps(crypto_data))

        if len(dataset) > 0 and len(dataset['rs']) > 0:
            return {'success': True, 'message': dataset['rs'].iloc[0].loc['message']}
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
