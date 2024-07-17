from decimal import Decimal

import requests
from eth_account import Account
from fastapi import APIRouter, Depends
from web3 import Web3, HTTPProvider

from src.misc.constants.messages import (DATABASE_CONNECTION_ERROR, OK)
from src.misc.security.Jwt import get_current_user
from src.misc.security.RightsChecker import RightsChecker
from src.utilities.utils import get_error_message, config

router = APIRouter()

crypto_payment_gateway_config = config['CryptoPaymentGateway']

network = "Binance"
binance_chain_id = 56
api_keys = [
    {"key": 'RWISWAUD35N3CB6SZTYUI8I6CET2RT2WG2', 'used_count': 0},
    {"key": 'A256IHPNIMTEJG7D61ZHXICDFGGTNA3SKB', 'used_count': 0}
]
provider_url = 'https://bsc-dataseed.binance.org/'
erc20_token_contract_abi = [
                                {
                                    "constant": False,
                                    "inputs": [
                                        {"name": "_to", "type": "address"},
                                        {"name": "_value", "type": "uint256"}
                                    ],
                                    "name": "transfer",
                                    "outputs": [{"name": "", "type": "bool"}],
                                    "payable": False,
                                    "stateMutability": "nonpayable",
                                    "type": "function"
                                },
                                {
                                    "constant": True,
                                    "inputs": [
                                        {
                                            "name": "_owner",
                                            "type": "address"
                                        }
                                    ],
                                    "name": "balanceOf",
                                    "outputs": [
                                        {
                                            "name": "balance",
                                            "type": "uint256"
                                        }
                                    ],
                                    "payable": False,
                                    "stateMutability": "view",
                                    "type": "function"
                                }
                            ]

@router.get('/get_withdrawal_currencies', dependencies=[Depends(RightsChecker([222]))])
async def get_withdrawal_currencies(token_payload: any = Depends(get_current_user)):
    try:
        response = requests.get(crypto_payment_gateway_config['BaseURL']+'get_withdrawal_currencies?app_key='+crypto_payment_gateway_config['AppKey'])

        data = response.json()

        # print(data)
        if data['success']:
            return {'success': True, 'message': OK, 'data': data['data'] }

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


def send_token_on_binance(private_key: str, to_address: str, amount: Decimal, token_contract_address: str, decimals: int, max_fee: Decimal=None):
    try:
        w3 = Web3(HTTPProvider(provider_url))
        # w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        if not w3.is_connected():
            raise Exception("Failed to connect to the network")

        # ERC-20 transfer function ABI
        abi = erc20_token_contract_abi

        # Set up the contract
        contract = w3.eth.contract(address=Web3.to_checksum_address(token_contract_address), abi=abi)

        # Prepare transaction
        account = Account.from_key(private_key)
        nonce = w3.eth.get_transaction_count(account.address)
        amount = int(amount * (10 ** decimals))  #amount_in_smallest_unit(amount=amount, decimals=decimals)

        balance = contract.functions.balanceOf(account.address).call()
        if balance < amount:
            return {'success': False, 'message': 'Insufficient token balance!'}

        gas_price = w3.eth.gas_price
        gas_estimate = contract.functions.transfer(Web3.to_checksum_address(to_address), amount).estimate_gas(
            {'from': account.address})

        fee = Decimal(w3.from_wei(gas_price * gas_estimate, 'ether'))
        if max_fee is not None and max_fee > 0:
            if fee > max_fee:
                return {'success': False, 'message': 'Fee is too high!'}

        txn = contract.functions.transfer(
            Web3.to_checksum_address(to_address),
            amount  # Note: this amount should be in the smallest unit of the token (like Wei for ETH)
        ).build_transaction({
            'chainId': binance_chain_id,
            'gas': gas_estimate,
            'gasPrice': gas_price,
            'nonce': nonce,
        })

        # Sign the transaction
        signed_txn = w3.eth.account.sign_transaction(txn, private_key)

        # Send the transaction
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Wait for confirmation
        txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

        # return txn_receipt
        return {'success': True, 'message': OK,
                'data': {'transaction_hash': txn_hash.hex(), 'success_status': txn_receipt['status'] == 1}}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
