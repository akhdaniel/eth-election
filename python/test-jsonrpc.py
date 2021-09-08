import odoorpc
import requests
import json

odoo = odoorpc.ODOO('remcash.vitraining.com')
odoo.login('remcash.vitraining.com', 'admin', '1')

odoo.execute('res.company', 'add_candidate', ["Candidate 1"] )
