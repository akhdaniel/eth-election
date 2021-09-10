# -*- coding: utf-8 -*-
from web3 import Web3
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class res_company(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'

    def bsc_connect(self):
        
        ICP = self.env['ir.config_parameter'].sudo()
        ABI = ICP.get_param('vit_election.abi')
        BSC = ICP.get_param('vit_election.bsc_url')
        CONTRACT_ADDRESS=ICP.get_param('vit_election.contract_address')
        ACCOUNT_ADDRESS_1=ICP.get_param('vit_election.system_address')
        PRIVATE_KEY_1=ICP.get_param('vit_election.system_private_key')
        CHAIN_ID=ICP.get_param('vit_election.chain_id')

        web3 = Web3(Web3.HTTPProvider(BSC))
        contract_address = web3.toChecksumAddress(CONTRACT_ADDRESS)
        contract = web3.eth.contract(address=contract_address, abi=ABI)   
        my_account = web3.toChecksumAddress(ACCOUNT_ADDRESS_1)
        my_private_key = PRIVATE_KEY_1

        res = "BSC connected: {}\n".format( web3.isConnected() )
        res += 'candidatesCount={}\n'.format( contract.functions.candidatesCount().call())
        res += 'candidates(1)={}\n'.format(contract.functions.candidates(1).call())
        res += 'nonce={}\n'.format( web3.eth.get_transaction_count(self.my_account))
        res += 'gasPrice={}\n'.format(web3.eth.gas_price)
        _logger.info('bsc_test_connection: %s', res)

        return web3,contract,my_account,my_private_key,CHAIN_ID

    def bsc_add_candidate(self, candidate_name, voting_session_id):
        try:
            web3,contract,my_account,my_private_key,chain_id = self.bsc_connect(self)
            transaction = contract.functions.addCandidate(candidate_name, voting_session_id).buildTransaction({
                    'chainId': chain_id,
                    'gas': 1000000,
                    'gasPrice': web3.eth.gasPrice,
                    'nonce': web3.eth.getTransactionCount(my_account)
                    })

            signed_txn = web3.eth.account.signTransaction(transaction, my_private_key)
            tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

            return {
                'status': 0,
                'rx_receipt': str(tx_receipt)
            }
            
        except Exception as e:
            return {
                'status': -1,
                'message': str(e)
            }

    def bsc_add_voter(self, voter_name):
        try:
            account = self.bsc_create_account(voter_name)
            voter_address = account.address

            transaction = contract.functions.addVoter(voter_name, voter_address).buildTransaction({
                    'chainId': CHAIN_ID,
                    'gas': 1000000,
                    'gasPrice': web3.eth.gasPrice,
                    'nonce': web3.eth.getTransactionCount(my_account)
                    })

            signed_txn = web3.eth.account.signTransaction(transaction, my_private_key)
            tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            return {
                'status': 0,
                'address': str(account.address),
                'private_key': str(account.privateKey),
                'rx_receipt': str(tx_receipt)
            }
            
        except Exception as e:
            return {
                'status': -1,
                'message': str(e)
            }

    def bsc_vote(self, candidate_id, voter_address, voting_session_id):
        try:
            web3,contract,my_account,my_private_key,chain_id = self.bsc_connect(self)
            transaction = contract.functions.vote(candidate_id, voter_address, voting_session_id).buildTransaction({
                    'chainId': chain_id,
                    'gas': 1000000,
                    'gasPrice': web3.eth.gasPrice,
                    'nonce': web3.eth.getTransactionCount(my_account)
                    })

            signed_txn = web3.eth.account.signTransaction(transaction, my_private_key)
            tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            return {
                'status': 0,
                'rx_receipt': str(tx_receipt)
            }

        except Exception as e:
            return {
                'status': -1,
                'message': str(e)
            }

    def bsc_create_account(self, name):
        try:
            web3,contract,my_account,my_private_key,chain_id = self.bsc_connect(self)
            account = web3.eth.account.create(name)
            return account
        except Exception as e:
            return {
                'status': -1,
                'message': e
            }

