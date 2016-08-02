# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Product Cost Utilities",
    "version": "8.0.1.0.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "OdooMRP team, "
              "AvanzOSC",
    "website": "http://www.odoomrp.com",
    "contributors": [
        "Esther Martín <esthermartin@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "depends": [
        "mrp_production_estimated_cost",
        "product_variant_cost_price",
    ],
    "data": [
        "views/product_view.xml",
    ],
    "installable": True,
}
