#!/usr/bin/python
#-*- coding: utf-8 -*-

STATES = [('draft','New'),('open','Pending'),('done','Validated')]
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

import logging
_logger = logging.getLogger(__name__)



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
        res = self.env['res.company'].bsc_vote(self.candidate_id.address, self.voter_id.address, self.voting_session_id.id)
        # _logger.info('res = %s', res)
        
        if res['status'] == -1:
            raise UserError(res['message'])

        self.rx_receipt = res['rx_receipt']   



    def action_draft(self):
        self.state = STATES[0][0]

    def unlink(self):
        for me_id in self :
            if me_id.state != STATES[0][0]:
                raise UserError("Cannot delete non draft record!")
        return super(vote_record, self).unlink()
