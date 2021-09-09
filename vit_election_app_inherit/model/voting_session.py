#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class voting_session(models.Model):
    _name = "vit.voting_session"
    _inherit = "vit.voting_session"
