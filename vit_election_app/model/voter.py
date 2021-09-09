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


    def vote(self, ):
        pass


