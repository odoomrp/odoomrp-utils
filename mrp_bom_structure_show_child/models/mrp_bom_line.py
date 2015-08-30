# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    @api.one
    def _compute_standard_price(self):
        try:
            template_std_price = self.product_template.standard_price
        except AttributeError:
            # This is in case mrp_product_variants module is not installed
            template_std_price = 0.0
        self.standard_price = (
            self.product_id.standard_price or template_std_price)

    @api.one
    def _compute_childs_standard_price(self):
        self.childs_standard_price = 0
        for line in self.child_line_ids:
            self.childs_standard_price += (line.standard_price +
                                           line.childs_standard_price)

    routing_id = fields.Many2one(
        'mrp.routing', string="Productive Process",
        related="bom_id.routing_id", store=True, readonly=True)
    standard_price = fields.Float(
        string='Cost Price', compute='_compute_standard_price',
        digits_compute=dp.get_precision('Product Price'))
    childs_standard_price = fields.Float(
        string='Childs Cost Price', compute='_compute_childs_standard_price',
        digits_compute=dp.get_precision('Product Price'))
