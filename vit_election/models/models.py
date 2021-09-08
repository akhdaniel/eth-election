# -*- coding: utf-8 -*-
from web3 import Web3
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

ABI="""[
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"name": "voteRecords",
		"outputs": [
			{
				"name": "addr",
				"type": "address"
			},
			{
				"name": "votingSessionId",
				"type": "uint256"
			},
			{
				"name": "candidateId",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
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
				"name": "votingSessionId",
				"type": "uint256"
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
		"constant": true,
		"inputs": [],
		"name": "voterCount",
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
		"constant": false,
		"inputs": [
			{
				"name": "_candidateId",
				"type": "uint256"
			},
			{
				"name": "_addr",
				"type": "address"
			},
			{
				"name": "_votingSessionId",
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
		"constant": false,
		"inputs": [
			{
				"name": "_name",
				"type": "string"
			},
			{
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "addVoter",
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
				"name": "name",
				"type": "string"
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
				"name": "_addr",
				"type": "address"
			},
			{
				"name": "_votingSessionId",
				"type": "uint256"
			}
		],
		"name": "alreadyVote",
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
		"constant": false,
		"inputs": [
			{
				"name": "_name",
				"type": "string"
			},
			{
				"name": "_votingSessionId",
				"type": "uint256"
			}
		],
		"name": "addCandidate",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
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
BSC = "https://data-seed-prebsc-1-s1.binance.org:8545/"
CONTRACT_ADDRESS="0x9CD043e4670eC6356c631A9b28C82e71D15E6b3f"
ACCOUNT_ADDRESS_1='0x53Abd70D632d2C0ba16f1481E37Dee11D45eaB5d'
PRIVATE_KEY_1='facc87a5ff3dcd83f567b2dff733baa073e2b5a284c9fed8e7809dc4f396388a'
CHAIN_ID=97

web3 = Web3(Web3.HTTPProvider(BSC))
contract_address = web3.toChecksumAddress(CONTRACT_ADDRESS)
contract = web3.eth.contract(address=contract_address, abi=ABI)   
my_account = web3.toChecksumAddress(ACCOUNT_ADDRESS_1)
my_private_key = PRIVATE_KEY_1

class res_company(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'

    def init(self):
        _logger.info("BSC connected: %s", web3.isConnected() )
        _logger.info('candidatesCounte=1',contract.functions.candidatesCount().call())
        _logger.info('candidates(1)=',contract.functions.candidates(1).call())
        _logger.info('nonce=', web3.eth.getTransactionCount(self.my_account))
        _logger.info('gasPrice=',web3.eth.gasPrice)

    def bsc_add_candidate(self, candidate_name, voting_session_id):
        try:
            
            transaction = contract.functions.addCandidate(candidate_name, voting_session_id).buildTransaction({
                'chainId': CHAIN_ID,
                'gas': 1000000,
                'gasPrice': web3.eth.gasPrice,
                'nonce': web3.eth.getTransactionCount(my_account)
            })

            signed_txn = web3.eth.account.signTransaction(transaction, private_key)
            tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            _logger.info('add_candidate tx_receipt=%s', tx_receipt)
            
        except Exception as e:
            raise UserError(e)

    def bsc_vote(self, candidate_id, voter_address, voting_session_id):
        try:

            transaction = contract.functions.vote(candidate_id, voter_address, voting_session_id).buildTransaction({
                    'chainId': CHAIN_ID,
                    'gas': 1000000,
                    'gasPrice': web3.eth.gasPrice,
                    'nonce': web3.eth.getTransactionCount(my_account)
                    })

            signed_txn = web3.eth.account.signTransaction(transaction, private_key)
            tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            _logger.info('tx_receipt=%s', tx_receipt)

        except Exception as e:
            raise UserError(e)        


    def create_account(self, name):
        account = web3.eth.account.create(name)
        return account

