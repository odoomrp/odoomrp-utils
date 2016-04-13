# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Sale Order Route",
    "version": "8.0.1.0.0",
    'author': 'OdooMRP team',
    'website': "http://www.odoomrp.com",
    'contributors': ["Ainara Galdona <ainaragaldona@avanzosc.es>",
                     "Ana Juaristi <anajuaristi@avanzosc.es>"],
    "depends": [
        'sale_stock',
        'web_context_tunnel'
    ],
    "category": "Sales Management",
    "data": ['views/sale_order_view.xml'],
    "installable": True
}
