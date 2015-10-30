# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín <esthermartin@avanzosc.es> - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Sale Order Line Propagate Date",
    "version": "8.0.1.0",
    "author": "OdooMRP team, "
              "AvanzOSC, "
              "Serv. Tecnol. Avanzados - Pedro M. Baeza",
    "website": "www.odoomrp.com",
    "category": "Sales Management",
    "license": "AGPL-3",
    "contributors": ["Esther Martín <esthermartin@avanzosc.es>",
                     "Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>",
                     "Ana Juaristi <anajuaristi@avanzosc.es>"],
    "depends": ["sale_order_line_view", "sale_order_line_dates"],
    "data": ["views/res_partner.xml",
             "views/sale_order_line.xml"],
    "installable": True
}
