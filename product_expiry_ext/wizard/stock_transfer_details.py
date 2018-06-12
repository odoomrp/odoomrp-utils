# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import fields, models


class TransferDetailsItems(models.TransientModel):
    _inherit = 'stock.transfer_details_items'

    life_date = fields.Datetime(string='Life Date', related='lot_id.life_date')
