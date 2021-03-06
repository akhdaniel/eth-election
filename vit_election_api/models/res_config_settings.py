# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    vit_election_contract_address = fields.Char(
        string="Smart Contract Address",
        config_parameter="vit_election.contract_address",
        help="Ethereum smart contract address for e-voting."
    )

    vit_election_system_address = fields.Char(
        string="System Address",
        config_parameter="vit_election.system_address",
        help="System address for paying gas fees."
    )


    vit_election_chain_id = fields.Integer(
        string="Chain ID",
        config_parameter="vit_election.chain_id",
        help="Ethereum RPC Chain ID."
    )

    vit_election_bsc_url = fields.Char(
        string="Ethereum RPC URL",
        config_parameter="vit_election.bsc_url",
        help="Ethereum RPC URL."
    )

    vit_election_abi = fields.Char(
        string="Smart contract ABI",
        config_parameter="vit_election.abi",
        help="Smart contract ABI."
    )

