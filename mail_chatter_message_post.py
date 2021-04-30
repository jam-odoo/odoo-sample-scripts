# -*- coding: utf-8 -*-
# Documentation : https://www.odoo.com/documentation/14.0/webservices/odoo.html

import pprint
import xmlrpc.client
from datetime import datetime

pp = pprint.PrettyPrinter(indent=4)

url = 'https://6051779-saas-14-1.runbot36.odoo.com'
db = '6051779-saas-14-1-all'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)
sub_ids = models.execute_kw(db, uid, password, 'sale.subscription', 'search', [[]])
print (sub_ids)

for sub in sub_ids:
    models.execute_kw(db, uid, password, 'sale.subscription', 'message_post', [[sub]], {'body': 'Bot Message', 'title': 'Botted Title'})