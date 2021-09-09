#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','New'),('open','Pending'),('done','Posted')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class vote_record(models.Model):

    _name = "vit.vote_record"
    _description = "vit.vote_record"
    name = fields.Char( required=True, default="New", readonly=True,  string="Name",  help="")
    state = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",  help="")
    tx_hash = fields.Char( string="Tx hash",  readonly=True, states={"draft" : [("readonly",False)]},  help="")


    voter_id = fields.Many2one(comodel_name="res.partner",  string="Voter",  readonly=True, states={"draft" : [("readonly",False)]},  help="")
    candidate_id = fields.Many2one(comodel_name="res.partner",  string="Candidate",  readonly=True, states={"draft" : [("readonly",False)]},  help="")

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_done(self):
        self.state = STATES[2][0]

    def action_draft(self):
        self.state = STATES[0][0]

    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(vote_record, self).unlink()
