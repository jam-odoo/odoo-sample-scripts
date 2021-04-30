# -*- coding: utf-8 -*-
# Documentation : https://www.odoo.com/documentation/14.0/webservices/odoo.html

import pprint
import xmlrpc.client
from datetime import datetime
from graphviz import Digraph
from collections import defaultdict

pp = pprint.PrettyPrinter(indent=4)

url = 'https://6051779-saas-14-1.runbot36.odoo.com'
db = '6051779-saas-14-1-all'
username = 'admin'
password = 'admin'


common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)
module_ids = models.execute_kw(db, uid, password, 'ir.module.module', 'search_read', [[('state', '=', 'installed')]], {'fields': ['id', 'name', 'dependencies_id']})
dependencies_ids = models.execute_kw(db, uid, password, 'ir.module.module.dependency', 'search_read', [[]], {'fields': ['id', 'depend_id']})

dependencies_ids = { dep['id']: dep for dep in dependencies_ids}


modules = { mod['id']: mod for mod in module_ids }


mode_graph = Digraph(comment='Odoo Apps')
for mod in modules:
    mode_graph.node(str(mod), str(modules[mod]['name']))

for mod in module_ids:
    for dep in mod.get('dependencies_id'):
        mode_graph.edge(str(dependencies_ids[dep]['depend_id'][0]), str(modules[mod['id']]['id']))
mode_graph.render('odoo-apps.gv')
