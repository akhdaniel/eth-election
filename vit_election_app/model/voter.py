#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class voter(models.Model):

    _name = "res.partner"
    _description = "res.partner"
    _inherit = "res.partner"

    is_voter = fields.Boolean( string="Is voter",  help="")
    address = fields.Char( string="Address",  help="")
    rx_receipt = fields.Text( string="Rx receipt",  help="")


    def vote(self, ):
        pass


    voter_vote_record_ids = fields.One2many(comodel_name="vit.vote_record",  inverse_name="voter_id",  string="Voter vote record",  help="")
