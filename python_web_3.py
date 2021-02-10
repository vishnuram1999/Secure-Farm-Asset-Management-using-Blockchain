import json
from web3 import Web3
from flask import Flask, render_template, request, jsonify
from datetime import date
import pyfirmata
import time

app = Flask(__name__)

def op(idValue, fruit, temperature, weight, noOfDays, flag):
    ganache_url = "http://127.0.0.1:7545" #url of local blockchain network
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    address = web3.toChecksumAddress("0xBd958A56c87A43AE34c4D0adBa2826F7F897Dccd") #Will convert an upper or lowercase Ethereum address to a checksum address
    abi = json.loads('[{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"string","name":"_fruitName","type":"string"},{"internalType":"uint256","name":"_temperature","type":"uint256"},{"internalType":"uint256","name":"_weight","type":"uint256"},{"internalType":"uint256","name":"_noOfDays","type":"uint256"},{"internalType":"bool","name":"_flag","type":"bool"}],"name":"addFruit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"fruitArray","outputs":[{"internalType":"string","name":"fruitName","type":"string"},{"internalType":"uint256","name":"temperature","type":"uint256"},{"internalType":"uint256","name":"weight","type":"uint256"},{"internalType":"uint256","name":"noOfDays","type":"uint256"},{"internalType":"bool","name":"flag","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"output","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"threshold_value_checking","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
    contract = web3.eth.contract(address = address, abi = abi)
    dateOfCultivated = date.today()
    tx_hash = contract.functions.addFruit(idValue, fruit, temperature, weight, noOfDays, flag).transact()
    web3.eth.waitForTransactionReceipt(tx_hash) #Wait for the transaction to be mined, and get the transaction receipt
    dateOfPurchasing = date(2021, 2, 24)
    #noOfDaysItHasBeen =  dateOfPurchasing-dateOfCultivated
    contract.functions.threshold_value_checking(idValue).transact() #contract.functions.threshold_value_checking(idValue, noOfDaysItHasBeen.days).transact()
    return contract.functions.output(idValue).call()


@app.route('/')

def home():
    return render_template('index.html')

@app.route('/join', methods=['GET','POST'])

def my_form_post():
    text1 = request.form['text1']
    text2 = request.form['text2']
    text3 = request.form['text3']
    text4 = request.form['text4']
    text5 = request.form['text5']
    text6 = request.form['text6']
    
    combine = op(int(text1),str(text5),int(text2),int(text3),int(text4),bool(text6))
    result = {
        "output": combine
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)