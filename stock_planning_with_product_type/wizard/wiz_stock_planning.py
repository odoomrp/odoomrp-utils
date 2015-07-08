# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields


class WizStockPlanning(models.TransientModel):
    _inherit = 'wiz.stock.planning'

    product_type = fields.Many2one(
        'product.product.type', 'Product Type',
        help='Enter this field if you want to filter by product type')

    def _select_moves_to_try(self, fdate, from_date):
        moves = super(WizStockPlanning, self)._select_moves_to_try(
            fdate, from_date)
        if self.product_type:
            moves = moves.filtered(
                lambda x: x.product_id.product_tmpl_id.product_type.id ==
                self.product_type.id)
        return moves

    def _select_procurements_to_try(self, fdate, from_date):
        procurements = super(
            WizStockPlanning, self)._select_procurements_to_try(fdate,
                                                                from_date)
        if self.product_type:
            procurements = procurements.filtered(
                lambda x: x.product_id.product_tmpl_id.product_type.id ==
                self.product_type.id)
        return procurements
