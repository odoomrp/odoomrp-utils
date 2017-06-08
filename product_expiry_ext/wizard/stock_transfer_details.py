# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import fields, models


class TransferDetailsItems(models.TransientModel):
    _inherit = 'stock.transfer_details_items'

    removal_date = fields.Datetime(string='Removal Date', related='lot_id.removal_date')
