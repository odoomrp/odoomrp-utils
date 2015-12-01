# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, api, exceptions, _


class WizardSaleorderWf(models.TransientModel):
    _name = 'wizard.saleorder.wf'
    _description = 'Wizard Sale Order Workflow Finish'

    @api.multi
    def saleorder_finish_wf(self):
        active_id = self.env.context.get('active_id', False)
        if not active_id:
            return
        order = self.env['sale.order'].browse(active_id)
        if order.state in ('draft', 'done', 'cancel'):
            raise exceptions.Warning(_("Cannot process already processed "
                                       "or in 'draft' state order."))
        elif order.picking_ids.filtered(lambda x:
                                        x.state not in ('cancel', 'done')):
            raise exceptions.Warning(_("The order has no processed picking."))
        elif order.invoice_ids.filtered(lambda x:
                                        x.state not in ('cancel', 'paid')):
            raise exceptions.Warning(_("The order has no processed invoices."))
        order.delete_workflow()
        order.state = 'done'
