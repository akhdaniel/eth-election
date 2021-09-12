#!/usr/local/bin/python3

import requests
import json

import xmlrpc.client
url = "https://remcash.vitraining.com"
db = "remcash.vitraining.com"
username = "admin"
password = "e1fd1e33b3df8b05a7d04c727a1a95fbf16601c2"

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})


models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# # # add new candidate
# res = models.execute_kw(db, uid, password,
#     'res.company', 'bsc_add_candidate', [False, 'Test Candidate 1', 1]
#     )
# print(res)

# # add new voter, auto created account
# res = models.execute_kw(db, uid, password,
#     'res.company', 'bsc_add_voter', [False, 'Voter 200']
#     )
# print(res)

# add new voter, auto created account
# candidate_address = '0xfB176Ea72b011cdD2bE62417A242Fc3166218B3b'
# voter_address = '0x000230Ae6b4e407439DcD30A76a62f23719ed71A'
# voting_session_id = 1

# res = models.execute_kw(db, uid, password,
#     'res.company', 'bsc_vote', [False, candidate_address, voter_address, voting_session_id]
#     )
# print(res)

# # add new candidate
res = models.execute_kw(db, uid, password,
    'res.company', 'bsc_get_candidates', [False, 1]
    )
print(res)
