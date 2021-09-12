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
    candidate_id = fields.Integer( string="Candidate",  help="")


    voting_session_id = fields.Many2one(comodel_name="vit.voting_session",  string="Voting session",  help="")
    candidate_vote_record_ids = fields.One2many(comodel_name="vit.vote_record",  inverse_name="candidate_id",  string="Candidate vote record",  help="")
