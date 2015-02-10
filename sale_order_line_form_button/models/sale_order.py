# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, api, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def button_save_data(self):
        return True

    @api.multi
    def button_details(self):
        context = self.env.context.copy()
        context['view_buttons'] = True
        view = {
            'name': _('Details'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order.line',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'readonly': True,
            'res_id': self.id,
            'context': context
        }
        return view
