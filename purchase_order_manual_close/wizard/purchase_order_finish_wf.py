# -*- coding: utf-8 -*-
# (c) 2015 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api, exceptions, _


class PurchaseOrderFinishWf(models.TransientModel):
    _name = 'purchase.order.finish.wf'
    _description = 'Wizard Purchase Order Workflow Finish'

    @api.multi
    def end_workflow(self):
        active_id = self.env.context.get('active_id', False)
        if not active_id:
            return
        order = self.env['purchase.order'].browse(active_id)
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
