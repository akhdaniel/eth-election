#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

import logging
_logger = logging.getLogger(__name__)


class voting_result(models.Model):

    _name = "vit.voting_result"
    _inherit = "vit.voting_result"

    def action_get_result(self):
        res = self.env['res.company'].bsc_get_candidates()
        _logger.info('res = %s', res)
        if res['status'] == -1:
            raise UserError(res['message'])

        """
        struct Candidate {
            uint id;
            string name;
            uint votingSessionId;
            uint voteCount;
        }
        """
        for data in res['candidates']:
            candidate = self.env['res.partner'].search([('candidate_id','=',data[0])])
            self.create({
                'candidate_id': candidate.id,
                'voting_session_id': data[2],
                'vote_count': data[3],
            })

