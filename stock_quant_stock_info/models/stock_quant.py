# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields
from openerp.addons import decimal_precision as dp


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    cost = fields.Float(digits=dp.get_precision('Product Price'))
    inventory_value = fields.Float(digits=dp.get_precision('Product Price'))
    product_incoming_qty = fields.Float(
        string='Incoming Product', related='product_id.incoming_qty',
        help="Quantity of products that are planned to arrive.\n"
             "In a context with a single Stock Location, this includes "
             "goods arriving to this Location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods arriving to the Stock Location of this Warehouse, or "
             "any of its children.\n"
             "Otherwise, this includes goods arriving to any Stock "
             "Location with 'internal' type.")
    product_outgoing_qty = fields.Float(
        string='Outgoing Product', related='product_id.outgoing_qty',
        help="Quantity of products that are planned to leave.\n"
             "In a context with a single Stock Location, this includes "
             "goods leaving this Location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods leaving the Stock Location of this Warehouse, or "
             "any of its children.\n"
             "Otherwise, this includes goods leaving any Stock "
             "Location with 'internal' type.")
