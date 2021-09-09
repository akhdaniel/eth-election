#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('new','New'),('posted','Posted')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class vote_record(models.Model):
    _name = "vit.vote_record"
    _inherit = "vit.vote_record"

    @api.model
    def create(self, vals):
        if not vals.get("name", False) or vals["name"] == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("vit.vote_record") or "Error Number!!!"
        return super(vote_record, self).create(vals)

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
