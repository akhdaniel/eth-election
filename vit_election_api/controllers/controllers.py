# -*- coding: utf-8 -*-
# from odoo import http


# class VitElection(http.Controller):
#     @http.route('/vit_election/vit_election/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_election/vit_election/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_election.listing', {
#             'root': '/vit_election/vit_election',
#             'objects': http.request.env['vit_election.vit_election'].search([]),
#         })

#     @http.route('/vit_election/vit_election/objects/<model("vit_election.vit_election"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_election.object', {
#             'object': obj
#         })
