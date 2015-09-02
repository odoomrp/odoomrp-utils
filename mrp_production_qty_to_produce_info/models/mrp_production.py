# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.one
    def _get_quantity_info(self):
        self.pending_quantity_to_produce = sum(
            self.move_created_ids.mapped('product_qty'))
        produced = self.move_created_ids2.filtered(lambda x: x.state == 'done')
        self.quantity_produced = sum(produced.mapped('product_qty'))

    quantity_produced = fields.Float(
        string='Quantity produced', compute='_get_quantity_info',
        digits_compute=dp.get_precision('Product Unit of Measure'))
    pending_quantity_to_produce = fields.Float(
        string='Pending quantity to produce', compute='_get_quantity_info',
        digits_compute=dp.get_precision('Product Unit of Measure'))
