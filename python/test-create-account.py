from web3 import Web3
import ssl
import time, json
#bsc = "https://bsc-dataseed.binance.org/"
bsc = "https://data-seed-prebsc-1-s1.binance.org:8545/"
web3 = Web3(Web3.HTTPProvider(bsc))
print(web3.isConnected())

account = web3.eth.account.create("Candidate 1")
print(account)

