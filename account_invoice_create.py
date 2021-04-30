# -*- coding: utf-8 -*-
# Documentation : https://www.odoo.com/documentation/14.0/webservices/odoo.html

import timeit
import pprint
import random
import xmlrpc.client
from datetime import datetime
pp = pprint.PrettyPrinter(indent=4)


url = 'https://6868528-14-0-all.runbot33.odoo.com'
db = '6868528-14-0-all'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
uid = common.authenticate(db, username, password, {})
print ('Logged with user id : %s'%(uid))



# Taking sample record anmes for searching in canched object
company_name = 'My Company (San Francisco)'
currency_name = 'USD'
customer_name = 'Azure Interior'
account_code = '400000'
journal_name = 'Customer Invoices'
line_account_name = ''

start_time=timeit.default_timer()

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)

# cache all currencies
currencies = models.execute_kw(db, uid, password, 'res.currency', 'search_read', [[['active', '=', True]]], {'fields': ['name', 'id']})
currency_name_ids = { rec['name']: rec['id'] for rec in currencies}

#cacahe all companies
compaines = models.execute_kw(db, uid, password, 'res.company', 'search_read', [[]], {'fields': ['name', 'id']})
company_name_ids = { rec['name']: rec['id'] for rec in compaines}

# cache all customers
customers = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['active', '=', True]]], {'fields': ['name', 'id']})
customer_name_ids = { rec['name']: rec['id'] for rec in customers}

#cacahe all journals
journals = models.execute_kw(db, uid, password, 'account.journal', 'search_read', [[['type', '=', 'sale'], ['company_id', '=', company_name_ids[company_name]]]], {'fields': ['name', 'id']})
journal_name_ids = { rec['name']: rec['id'] for rec in journals}

# cache all accounts
accounts = models.execute_kw(db, uid, password, 'account.account', 'search_read', [[['company_id', '=', company_name_ids[company_name]]]], {'fields': ['name', 'code','id']})
account_name_ids = { rec['code']: rec['id'] for rec in accounts}

print('Time to cachae all records : ',timeit.default_timer()-start_time)

#reset time to see time after creation
start_time=timeit.default_timer()
#carete random ecord to load testing
for mi in range(random.randrange(10, 100)):
    #preapring lines
    move_lines = []
    lines_count = range(mi)
    for idx  in lines_count:
        move_lines.append({
            'sequence': 10+idx,
            'name': 'Line#%d/%d'%(mi, idx),
            'account_id': account_name_ids[account_code],
            'quantity': 1,
            'price_unit': 9.99,
        })


    move_vals = {
        'partner_id': customer_name_ids[customer_name],
        'partner_shipping_id':  customer_name_ids[customer_name],
        'journal_id': journal_name_ids[journal_name],
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'payment_state': 'not_paid',
        'name': '/',
        'invoice_payment_term_id': 7,
        'journal_id': journal_name_ids[journal_name],
        'currency_id': currency_name_ids[currency_name],
        'invoice_user_id': uid,
        'company_id': company_name_ids[company_name],
        'move_type': 'out_invoice',
        'invoice_line_ids': [(0, 0, ml) for ml in move_lines],
    }
    move_id = models.execute_kw(db, uid, password, 'account.move', 'create', [move_vals])
    print('Time from start of first record : ', timeit.default_timer()-start_time, 'for move with lines', lines_count)


print('Time after call record creation all records : ',timeit.default_timer()-start_time)
