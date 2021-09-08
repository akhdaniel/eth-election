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

class res_company(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'

    web3 = None
    contract = None
    my_account = None
    my_private_key = None

    def bsc_connect(self):
        self.web3 = Web3(Web3.HTTPProvider(BSC))
        self.my_account = self.web3.toChecksumAddress(ACCOUNT_ADDRESS_1)
        self.my_private_key = PRIVATE_KEY_1

        _logger.info("BSC connected: %s", self.web3.isConnected() )
        self.bsc_get_contract()
        return self.web3.isConnected()

    def bsc_get_contract(self):
        contract_address = self.web3.toChecksumAddress(CONTRACT_ADDRESS)
        self.contract = self.web3.eth.contract(address=contract_address, abi=ABI)        
        _logger.info('candidatesCounte=1',self.contract.functions.candidatesCount().call())
        _logger.info('candidates(1)=',self.contract.functions.candidates(1).call())
        _logger.info('nonce=', self.web3.eth.getTransactionCount(self.my_account))
        _logger.info('gasPrice=',self.web3.eth.gasPrice)

    def bsc_add_candidate(self, candidate_name, voting_session_id):
        try:
            if not self.bsc_connect():
                raise UserError('Failed to connect to BSC')
            
            transaction = self.contract.functions.addCandidate(candidate_name, voting_session_id).buildTransaction({
                'chainId': CHAIN_ID,
                'gas': 1000000,
                'gasPrice': self.web3.eth.gasPrice,
                'nonce': self.web3.eth.getTransactionCount(my_account)
            })

            signed_txn = self.web3.eth.account.signTransaction(transaction, self.private_key)
            tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
            _logger.info('add_candidate tx_receipt=%s', tx_receipt)
            
        except Exception as e:
            raise UserError(e)

    def bsc_vote(self, candidate_id, voter_address, voting_session_id):
        try:
            if not self.bsc_connect():
                raise UserError('Failed to connect to BSC')

            transaction = self.contract.functions.vote(candidate_id, voter_address, voting_session_id).buildTransaction({
                    'chainId': CHAIN_ID,
                    'gas': 1000000,
                    'gasPrice': self.web3.eth.gasPrice,
                    'nonce': self.web3.eth.getTransactionCount(my_account)
                    })

            signed_txn = self.web3.eth.account.signTransaction(transaction, self.private_key)
            tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
            _logger.info('tx_receipt=%s', tx_receipt)

        except Exception as e:
            raise UserError(e)        


    def create_account(self, name):
        account = self.web3.eth.account.create(name)
        return account

