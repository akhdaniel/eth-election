#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

import logging
_logger = logging.getLogger(__name__)



class voting_result(models.Model):

    _name = "vit.voting_result"

    def action_get_result(self):
        res = self.env['res.company'].bsc_get_candidates()
        _logger.info('res = %s', res)
        if res['status'] == -1:
            raise UserError(res['message'])
        self.rx_receipt = res['rx_receipt']        
