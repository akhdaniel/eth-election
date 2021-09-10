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
        abi = ICP.get_param('vit_election.abi')
        bsc = ICP.get_param('vit_election.bsc_url')
        contract_address = ICP.get_param('vit_election.contract_address')
        account_address_1 = ICP.get_param('vit_election.system_address')
        private_key_1 = ICP.get_param('vit_election.system_private_key')
        chain_id = int(ICP.get_param('vit_election.chain_id'))

        web3 = Web3(Web3.HTTPProvider(bsc))
        contract_address = web3.toChecksumAddress(contract_address)
        contract = web3.eth.contract(address=contract_address, abi=abi)   
        system_account = web3.toChecksumAddress(account_address_1)
        system_private_key = private_key_1

        res = "bsc connected: {}\n".format( web3.isConnected() )
        res += 'candidatesCount={}\n'.format( contract.functions.candidatesCount().call())
        # res += 'candidates(1)={}\n'.format(contract.functions.candidates(1).call())
        res += 'nonce={}\n'.format( web3.eth.get_transaction_count(system_account))
        res += 'gasPrice={}\n'.format(web3.eth.gas_price)
        _logger.info('bsc_test_connection: %s', res)

        return web3,contract,system_account,system_private_key,chain_id

    def bsc_add_candidate(self, candidate_name, voting_session_id):
        try:
            web3,contract,system_account,system_private_key,chain_id = self.bsc_connect()
            account = self.bsc_create_account(candidate_name)
            candidate_address = account.address

            transaction = contract.functions.addCandidate(candidate_name, candidate_address, voting_session_id).buildTransaction({
                    'chainId': chain_id,
                    'gas': 1000000,
                    'gasPrice': web3.eth.gasPrice,
                    'nonce': web3.eth.getTransactionCount(system_account)
                    })

            signed_txn = web3.eth.account.signTransaction(transaction, system_private_key)
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

    def bsc_add_voter(self, voter_name):
        try:
            web3,contract,system_account,system_private_key,chain_id = self.bsc_connect()
            account = self.bsc_create_account(voter_name)
            voter_address = account.address

            transaction = contract.functions.addVoter(voter_name, voter_address).buildTransaction({
                    'chainId': chain_id,
                    'gas': 1000000,
                    'gasPrice': web3.eth.gasPrice,
                    'nonce': web3.eth.getTransactionCount(system_account)
                    })

            signed_txn = web3.eth.account.signTransaction(transaction, system_private_key)
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

    def bsc_vote(self, candidate_address, voter_address, voting_session_id):
        try:
            web3,contract,system_account,system_private_key,chain_id = self.bsc_connect()
            transaction = contract.functions.vote(candidate_address, voter_address, voting_session_id).buildTransaction({
                    'chainId': chain_id,
                    'gas': 1000000,
                    'gasPrice': web3.eth.gasPrice,
                    'nonce': web3.eth.getTransactionCount(system_account)
                    })

            signed_txn = web3.eth.account.signTransaction(transaction, system_private_key)
            tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

            # _logger.info(dict(tx_receipt))
            
            if tx_receipt["status"] != 1:
                # raise UserError(tx_receipt)
                raise UserError("Error executing bsc_vote")

            return {
                'status': 0,
                'rx_receipt': str(tx_receipt),
                'voteRecordCount': contract.functions.voteRecordCount().call(),
            }

        except Exception as e:
            return {
                'status': -1,
                'message': str(e)
            }

    def bsc_create_account(self, name):
        try:
            web3,contract,system_account,system_private_key,chain_id = self.bsc_connect()
            account = web3.eth.account.create(name)
            return account
        except Exception as e:
            return {
                'status': -1,
                'message': e
            }

