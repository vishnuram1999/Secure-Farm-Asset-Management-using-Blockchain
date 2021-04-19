from web3 import Web3

ganache_url = "http://127.0.0.1:7545" #url of local blockchain network
web3 = Web3(Web3.HTTPProvider(ganache_url))

latest = web3.eth.blockNumber
#print(web3.eth.getBlock(latest))

for i in range(0, 7):
  print(web3.eth.getBlock(latest - i))