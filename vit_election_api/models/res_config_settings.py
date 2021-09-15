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

