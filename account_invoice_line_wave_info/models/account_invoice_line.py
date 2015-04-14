# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    wave_id = fields.Many2one(
        string='Picking Wave', comodel_name='stock.picking.wave',
        related='move.picking_id.wave_id', readonly=True)
