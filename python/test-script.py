from web3 import Web3
import ssl
import time, json
#bsc = "https://bsc-dataseed.binance.org/"
ABI="""[
	{
		"constant": false,
		"inputs": [
			{
				"name": "_candidateId",
				"type": "uint256"
			}
		],
		"name": "vote",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "candidatesCount",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"name": "candidates",
		"outputs": [
			{
				"name": "id",
				"type": "uint256"
			},
			{
				"name": "name",
				"type": "string"
			},
			{
				"name": "voteCount",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_name",
				"type": "string"
			}
		],
		"name": "addCandidate",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"name": "voters",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"name": "_candidateId",
				"type": "uint256"
			}
		],
		"name": "votedEvent",
		"type": "event"
	}
]
"""

CONTRACT_ADDRESS="0x204adB832E6306E17BE51bDd79429eb0689a2F89"

ACCOUNT_ADDRESS_1='0x53Abd70D632d2C0ba16f1481E37Dee11D45eaB5d'
PRIVATE_KEY_1='facc87a5ff3dcd83f567b2dff733baa073e2b5a284c9fed8e7809dc4f396388a'

ACCOUNT_ADDRESS_2='0x53144990db4f070c47924E447c4cb9ad52346f2c'
PRIVATE_KEY_2='e1b59edd0d94e5572847aa7daf181d929fae40ceffc49090bc2c6ec6a0dc8ed6'

CHAIN_ID=97

bsc = "https://data-seed-prebsc-1-s1.binance.org:8545/"
web3 = Web3(Web3.HTTPProvider(bsc))
print(web3.isConnected())

#accounts
my_account = web3.toChecksumAddress(ACCOUNT_ADDRESS_1)
private_key = PRIVATE_KEY_1

contract_address = web3.toChecksumAddress(CONTRACT_ADDRESS)
contract = web3.eth.contract(address=contract_address, abi=ABI)
print('candidatesCounte=1',contract.functions.candidatesCount().call())
print('candidates(1)=',contract.functions.candidates(1).call())
print('nonce=', web3.eth.getTransactionCount(my_account))
print('gasPrice=',web3.eth.gasPrice)

transaction = contract.functions.vote(1).buildTransaction({
                    'chainId': CHAIN_ID,
                    'gas': 1000000,
                    'gasPrice': web3.eth.gasPrice,
                    'nonce': web3.eth.getTransactionCount(my_account)
                    })

signed_txn = web3.eth.account.signTransaction(transaction, private_key)
tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
print(tx_receipt)

