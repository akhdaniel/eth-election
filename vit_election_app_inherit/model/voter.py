#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class voter(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    def vote(self, ):
        pass

    def action_create_account(self):
        pass