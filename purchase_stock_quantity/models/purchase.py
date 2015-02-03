
from openerp import models, fields


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    stock_quantity = fields.Float(comodel_name='product.product',
                                  related='product_id.virtual_available',
                                  string='Virtual Available')
