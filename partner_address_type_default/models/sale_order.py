# -*- coding: utf-8 -*-
# © 2015 AvanzOSC, Pedro M. Baeza, Sodexis, OdooMRP team
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        result = super(SaleOrder, self).onchange_partner_id()
        for line in self.partner_id.child_ids:
            if line.type == 'invoice' and line.default_address:
                self.partner_invoice_id = line.id
            if line.type == 'delivery' and line.default_address:
                self.partner_shipping_id = line.id
        return result
