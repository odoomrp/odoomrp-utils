# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        partner_obj = self.pool['res.partner']
        result = super(SaleOrder, self).onchange_partner_id(
            cr, uid, ids, part, context=context)
        partner = partner_obj.browse(cr, uid, part, context=context)
        value = result['value']
        if partner.child_ids:
            for line in partner.child_ids:
                if line.type == 'invoice' and line.default_address:
                    value['partner_invoice_id'] = line.id
                if line.type == 'delivery' and line.default_address:
                    value['partner_shipping_id'] = line.id
        result['value'] = value
        return result
