import json
from web3 import Web3
from flask import Flask, render_template, request, jsonify
from datetime import date
import pyfirmata
import time

app = Flask(__name__)

ganache_url = "http://127.0.0.1:7545" #url of local blockchain network
web3 = Web3(Web3.HTTPProvider(ganache_url))
web3.eth.defaultAccount = web3.eth.accounts[0]
address = web3.toChecksumAddress("0x90Bb5Db737F347249DA94Ed4D0448e8A8ED3Eff9") #Will convert an upper or lowercase Ethereum address to a checksum address
abi = json.loads('[{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"string","name":"_fruitName","type":"string"},{"internalType":"uint256","name":"_temperature","type":"uint256"},{"internalType":"uint256","name":"_weight","type":"uint256"},{"internalType":"uint256","name":"_noOfDays","type":"uint256"},{"internalType":"string","name":"_price","type":"string"}],"name":"addFruit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"assetArray","outputs":[{"internalType":"string","name":"asset_name","type":"string"},{"internalType":"uint256","name":"day","type":"uint256"},{"internalType":"uint256","name":"month","type":"uint256"},{"internalType":"uint256","name":"year","type":"uint256"},{"internalType":"bool","name":"flag","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"string","name":"_asset_name","type":"string"},{"internalType":"uint256","name":"_day","type":"uint256"},{"internalType":"uint256","name":"_month","type":"uint256"},{"internalType":"uint256","name":"_year","type":"uint256"}],"name":"book_asset","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"uint256","name":"_day","type":"uint256"},{"internalType":"uint256","name":"_month","type":"uint256"},{"internalType":"uint256","name":"_year","type":"uint256"}],"name":"check_asset","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"fruitArray","outputs":[{"internalType":"string","name":"fruitName","type":"string"},{"internalType":"uint256","name":"temperature","type":"uint256"},{"internalType":"uint256","name":"weight","type":"uint256"},{"internalType":"uint256","name":"noOfDays","type":"uint256"},{"internalType":"bool","name":"flag","type":"bool"},{"internalType":"string","name":"price","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"output","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"print","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"print1","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"uint256","name":"_expiryDays","type":"uint256"}],"name":"threshold_value_checking","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
contract = web3.eth.contract(address = address, abi = abi)

def op(idValue, fruit, temperature, weight, noOfDays, price):
    dateOfCultivated = date.today()
    tx_hash = contract.functions.addFruit(idValue, fruit, temperature, weight, noOfDays, price).transact()
    web3.eth.waitForTransactionReceipt(tx_hash) #Wait for the transaction to be mined, and get the transaction receipt
    contract.functions.threshold_value_checking(idValue, 0).transact() 
    return contract.functions.output(idValue).call()

def op1(idValue):    
    dateOfPurchasing = date(2021, 3, 17) #date.today()
    dateOfCultivated = date.today()
    noOfDaysItHasBeen =  dateOfPurchasing-dateOfCultivated
    contract.functions.threshold_value_checking(idValue, noOfDaysItHasBeen.days).transact() #contract.functions.threshold_value_checking(idValue, noOfDaysItHasBeen.days).transact()
    return contract.functions.output(idValue).call()

def op2(idValue, day, month, year):
    contract.functions.book_asset(idValue, "Machinery", day, month, year).transact()
    return contract.functions.print(idValue).call()

def op3(idValue, day, month, year):
    contract.functions.check_asset(idValue, day, month, year).transact()
    return contract.functions.print1(idValue).call()


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
    text7 = request.form['text7']
    
    combine = op(int(text1), str(text5), int(text2), int(text3), int(text4), str(text7))
    result = {
        "output": combine
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

@app.route('/join1', methods=['GET','POST'])

def my_output():
    text8 = request.form['text8']

    out = op1(int(text8))
    result1 = {
        "output": out
    }
    result1 = {str(key): value for key, value in result1.items()}
    return jsonify(result1=result1)

@app.route('/join2', methods=['GET','POST'])

def assets_booking():
    text9 = request.form['text9']
    text10 = request.form['text10']
    text11 = request.form['text11']
    text12 = request.form['text12']

    book = op2(int(text9), int(text10), int(text11), int(text12))
    result2 = {
        "output": book
    }
    result2 = {str(key): value for key, value in result2.items()}
    return jsonify(result2=result2)

@app.route('/join3', methods=['GET','POST'])

def assets_checking():
    text9 = request.form['text9']
    text10 = request.form['text10']
    text11 = request.form['text11']
    text12 = request.form['text12']

    book1 = op3(int(text9), int(text10), int(text11), int(text12))
    result3 = {
        "output": book1
    }
    result3 = {str(key): value for key, value in result3.items()}
    return jsonify(result3=result3)

if __name__ == '__main__':
    app.run(debug=True)
