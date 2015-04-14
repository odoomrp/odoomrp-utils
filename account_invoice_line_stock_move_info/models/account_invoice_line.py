# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    move = fields.Many2one('stock.move', string='Stock Move')
    picking_id = fields.Many2one(
        string='Picking', comodel_name='stock.picking',
        related='move.picking_id', readonly=True)
