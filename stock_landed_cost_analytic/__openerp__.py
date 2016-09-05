# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Stock Landed Cost Analytic",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ainara Galdona <ainaragaldona@avanzosc.es>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
    ],
    "category": "Warehouse Management",
    "depends": [
        "analytic",
        "stock_landed_costs"
    ],
    "data": [
        "wizard/landed_cost_import_lines_view.xml",
        "views/stock_landed_cost_view.xml",
        "views/account_invoice_view.xml"
    ],
    "installable": True,
}
