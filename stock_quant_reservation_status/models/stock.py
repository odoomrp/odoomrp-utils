# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields, api


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.one
    @api.depends('reservation_id')
    def _is_reserved(self):
        self.is_reserved = bool(self.reservation_id)

    is_reserved = fields.Boolean(
        string='Reserved Quant', compute='_is_reserved', store=True)
