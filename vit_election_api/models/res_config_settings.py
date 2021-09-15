# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    vit_election_contract_address = fields.Char(
        string="Smart Contract Address",
        help="Ethereum smart contract address for e-voting."
    )

    vit_election_system_address = fields.Char(
        string="System Address",
        help="System address for paying gas fees."
    )


    vit_election_chain_id = fields.Integer(
        string="Chain ID",
        help="System address for paying gas fees."
    )

    vit_election_bsc_url = fields.Char(
        string="Ethereum RPC URL",
        help="System address for paying gas fees."
    )


    vit_election_abi = fields.Text(
        string="System Address",
        help="System address for paying gas fees."
    )

