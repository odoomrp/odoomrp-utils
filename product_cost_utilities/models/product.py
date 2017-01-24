# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, fields
import openerp.addons.decimal_precision as dp


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    @api.depends('list_price', 'standard_price')
    def _compute_average_margin(self):
        for product in self:
            product.average_margin =\
                product.list_price - product.standard_price

    @api.multi
    @api.depends('list_price', 'manual_standard_cost')
    def _compute_manual_margin(self):
        for product in self:
            product.manual_margin = \
                product.list_price - product.manual_standard_cost

    @api.multi
    @api.depends('standard_price', 'manual_standard_cost')
    def _compute_cost(self):
        for product in self:
            product.cost = \
                product.manual_standard_cost - product.standard_price

    average_margin = fields.Float(
        digits=dp.get_precision('Product Price'),
        compute='_compute_average_margin', store=True)
    manual_margin = fields.Float(
        digits=dp.get_precision('Product Price'),
        compute='_compute_manual_margin', store=True)
    cost = fields.Float(
        digits=dp.get_precision('Product Price'),
        compute='_compute_cost', store=True,
        help='Difference between manual standard and standard price')
    min_margin = fields.Float(string="Min. Margin",
                              digits=dp.get_precision('Product Price'))
