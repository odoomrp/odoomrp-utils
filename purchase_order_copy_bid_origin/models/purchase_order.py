# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    origin = fields.Char(copy=True)
    requisition_id = fields.Many2one(copy=True)
