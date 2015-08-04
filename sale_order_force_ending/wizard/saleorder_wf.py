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
            for sale_id in context['active_ids']:
                sale = sale_obj.browse(sale_id)
                if sale.state in ('draft', 'done', 'cancel'):
                    raise exceptions.Warning(
                        _("Selected Sale Orders cannot be processed!"))
                else:
                    workflow.trg_delete(self.env.uid, 'sale.order', sale_id,
                                        self.env.cr)
                    sale.state = 'done'
