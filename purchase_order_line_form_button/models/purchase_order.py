# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, api, _


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.multi
    def button_save_data(self):
        return True

    @api.multi
    def button_details(self):
        context = self.env.context.copy()
        view_id = self.env.ref(
            'purchase_order_line_form_button.'
            'purchase_order_line_button_form_view').id
        context['view_buttons'] = True
        context['parent'] = self.order_id.id
        view = {
            'name': _('Details'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.order.line',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'readonly': True,
            'res_id': self.id,
            'context': context
        }
        return view
