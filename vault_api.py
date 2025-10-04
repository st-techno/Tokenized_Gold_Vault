# vault_api.py

import os
from flask import Flask, request, jsonify
from web3 import Web3
import logging

# ABI for Chainlink AggregatorV3Interface (simplified for price reads)
aggregatorV3InterfaceABI = [
    {
        "inputs": [],
        "name": "latestRoundData",
        "outputs": [
            {"internalType": "uint80", "name": "roundId", "type": "uint80"},
            {"internalType": "int256", "name": "answer", "type": "int256"},
            {"internalType": "uint256", "name": "startedAt", "type": "uint256"},
            {"internalType": "uint256", "name": "updatedAt", "type": "uint256"},
            {"internalType": "uint80", "name": "answeredInRound", "type": "uint80"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Mainnet Chainlink price feed address for GOLD/USD: replace with the live address per docs
CHAINLINK_GOLD_FEED_ADDR = os.getenv("CHAINLINK_GOLD_FEED_ADDR", "0x214ed9C74c6c7E0Fae2f1A91d2A8efc5dD2fD4f9")

w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER')))
VAULT_CONTRACT = w3.eth.contract(address=os.getenv('VAULT_ADDRESS'), abi=os.getenv('VAULT_ABI'))
USER_PRIVATE_KEY = os.getenv('USER_PRIVATE_KEY')
logging.basicConfig(filename='vault.log', level=logging.INFO)

def get_gold_price_from_chainlink():
    feed = w3.eth.contract(address=CHAINLINK_GOLD_FEED_ADDR, abi=aggregatorV3InterfaceABI)
    round_data = feed.functions.latestRoundData().call()
    price = round_data[1] / 10 ** 8  # Chainlink returns price with 8 decimals
    return price

app = Flask(__name__)

@app.route('/price', methods=['GET'])
def get_gold_price():
    price = get_gold_price_from_chainlink()
    return jsonify({'gold_price': price})

@app.route('/deposit', methods=['POST'])
def deposit():
    user_address = request.json['address']
    amount = request.json['amount']
    tx = VAULT_CONTRACT.functions.deposit(amount, user_address).build_transaction({
        'nonce': w3.eth.get_transaction_count(user_address)
    })
    signed_tx = w3.eth.account.sign_transaction(tx, USER_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    logging.info(f"Deposit: {amount} tokens from {user_address}")
    return jsonify({'tx_hash': tx_hash.hex()})

@app.route('/withdraw', methods=['POST'])
def withdraw():
    user_address = request.json['address']
    shares = request.json['shares']
    tx = VAULT_CONTRACT.functions.withdraw(shares, user_address).build_transaction({
        'nonce': w3.eth.get_transaction_count(user_address)
    })
    signed_tx = w3.eth.account.sign_transaction(tx, USER_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    logging.info(f"Withdraw: {shares} shares from {user_address}")
    return jsonify({'tx_hash': tx_hash.hex()})

@app.route('/rebalance', methods=['POST'])
def rebalance():
    threshold = request.json.get('threshold', 0.8)
    price = get_gold_price_from_chainlink()
    logging.info(f"Rebalance trigger at price {price} with threshold {threshold}")
    return jsonify({'status': 'Rebalanced', 'price': price})

@app.route('/backtest', methods=['POST'])
def backtest():
    data = request.json['historical_prices']
    return jsonify({'results': 'backtest results here'})

if __name__ == '__main__':
    app.run(debug=True)
