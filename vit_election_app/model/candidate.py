#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class candidate(models.Model):

    _name = "res.partner"
    _description = "res.partner"
    _inherit = "res.partner"

    is_candidate = fields.Boolean( string="Is candidate",  help="")
    vote_count = fields.Integer( string="Vote count",  help="")


    voting_session_id = fields.Many2one(comodel_name="vit.voting_session",  string="Voting session",  help="")
