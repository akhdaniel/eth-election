#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class voting_session(models.Model):

    _name = "vit.voting_session"
    _description = "vit.voting_session"
    name = fields.Char( required=True, string="Name",  help="")
    description = fields.Text( string="Description",  help="")
    date_start = fields.Datetime( string="Date start",  help="")
    date_end = fields.Datetime( string="Date end",  help="")


    candidate_ids = fields.One2many(comodel_name="res.partner",  inverse_name="voting_session_id",  string="Candidate",  help="")
    vote_record_ids = fields.One2many(comodel_name="vit.vote_record",  inverse_name="voting_session_id",  string="Vote record",  help="")
