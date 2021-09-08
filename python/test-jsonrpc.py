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

res = models.execute_kw(db, uid, password,
    'res.company', 'bsc_add_candidate',
    ['Candidate 1', 1], {'raise_exception': False})
print(res)
