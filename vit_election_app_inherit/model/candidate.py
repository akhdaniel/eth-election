#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

import logging
_logger = logging.getLogger(__name__)


class candidate(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    def action_add_candidate(self):
        if not self.voting_session_id:
            raise UserError('voting session cannot empty!')
        res = self.env['res.company'].bsc_add_candidate(self.name, self.voting_session_id.id)
        _logger.info('res = %s', res)
        if res['status'] == -1:
            raise UserError(res['message'])
        self.rx_receipt = res['rx_receipt']
        # self.address = res['address']
        self.candidate_id = res['candidate_id']