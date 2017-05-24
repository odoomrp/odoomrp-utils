
# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api, exceptions, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def unlink(self):
        if (any([x and x != 'cancel' for x in
                self.mapped('invoice_line.picking_id.state')]) and
                any([x.state != 'cancel' for x in self])):
            raise exceptions.Warning(
                _('Before deleting invoices you should cancel them or cancel '
                  'next picking(s): %s.')
                % self.mapped('invoice_line.picking_id.name'))
        return super(AccountInvoice, self).unlink()

    @api.multi
    def action_cancel(self):
        res = super(AccountInvoice, self).action_cancel()
        self.mapped('invoice_line.picking_id').write(
            {'invoice_state': '2binvoiced'})
        return res

    @api.multi
    def action_cancel_draft(self):
        # go from canceled state to draft state
        res = super(AccountInvoice, self).action_cancel_draft()
        self.mapped('invoice_line.picking_id').write(
            {'invoice_state': 'invoiced'})
        return res


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    move = fields.Many2one('stock.move', string='Stock Move')
    picking_id = fields.Many2one(
        string='Picking', comodel_name='stock.picking',
        related='move.picking_id', readonly=True)
