#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

import logging
_logger = logging.getLogger(__name__)



class voter(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    def vote(self, ):
        pass

    def action_create_account(self):
        res = self.env['res.company'].bsc_create_account(self.name)
        _logger.info('res = %s', res)
        self.address = res.address