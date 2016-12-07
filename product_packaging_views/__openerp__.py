# -*- coding: utf-8 -*-
# Copyright 2014-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2014-2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3

{
    "name": "Product Packaging extended views",
    "version": "9.0.1.0.0",
    "depends": [
        "product",
    ],
    "author": "OdooMRP team,"
              "AvanzOSC,"
              "Tecnativa",
    "website": "http://www.odoomrp.com",
    "category": "Tools",
    "data": [
        "views/product_packaging_view.xml",
        "views/product_ul_view.xml",
        "views/product_view.xml",
        "security/ir.model.access.csv",
    ],
    'demo': [
        'demo/product_ul_demo.xml',
    ],
    'installable': True,
    'license': 'AGPL-3',
}
