# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, workflow, api, exceptions, _


class wizard_saleorder_wf(models.TransientModel):
    _name = 'wizard.saleorder.wf'
    _description = 'Wizard Sale Order Workflow'

    @api.multi
    def saleorder_finish_wf(self):
        sale_obj = self.env['sale.order']
        context = self.env.context
        if 'active_ids' in context:
            sale_orders = sale_obj.browse(context['active_ids'])
            for order in sale_orders:
                if order.state in ('draft', 'done', 'cancel'):
                    raise exceptions.Warning(
                        _("Selected Sale Orders cannot be processed as they "
                          "are already processed or in 'draft' state!"))
                workflow.trg_delete(self.env.uid, 'sale.order', order.id,
                                    self.env.cr)
            sale_orders.write({'state': 'done'})
