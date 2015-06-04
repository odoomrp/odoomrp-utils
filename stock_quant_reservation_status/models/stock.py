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
        self.reserved_for = (
            (self.reservation_id.picking_id.name or '') + ' ' +
            (self.reservation_id.origin or ''))

    is_reserved = fields.Boolean(
        string='Reserved Quant', compute='_is_reserved', store=True)
    reserved_for = fields.Char(
        string='Reserved for', compute='_is_reserved')
