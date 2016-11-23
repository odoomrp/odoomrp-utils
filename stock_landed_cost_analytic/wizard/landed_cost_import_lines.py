# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, _, api


class LandedCostImportInvoiceLines(models.TransientModel):

    _name = 'landed.cost.import.invoice.lines'

    invoice_line_ids = fields.Many2many(
        comodel_name='account.invoice.line',
        relation='rel_landed_invoice_line_import', string='Invoice Lines')

    @api.multi
    def get_landed_cost_line_values(self, invoice_line):
        self.ensure_one()
        return {
            'name': u'{} {}: {}'.format(
                _('INV'), invoice_line.invoice_id.number, invoice_line.name),
            'cost_id': self.env.context.get('active_id'),
            'product_id': invoice_line.product_id.id,
            'analytic_id': invoice_line.account_analytic_id.id,
            'price_unit': invoice_line.price_subtotal,
            'split_method': 'equal',
            'account_id': invoice_line.account_id.id,
        }

    @api.multi
    def import_lines(self):
        self.ensure_one()
        landed_cost_line_obj = self.env['stock.landed.cost.lines']
        for invoice_line in self.invoice_line_ids:
            landed_cost_line_obj.create(
                self.get_landed_cost_line_values(invoice_line))
        return {'type': 'ir.actions.act_window_close'}
