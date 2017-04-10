# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api, _


class StockLandedCost(models.Model):

    _inherit = 'stock.landed.cost'

    analytic_id = fields.Many2one(comodel_name='account.analytic.account',
                                  string='Analytic Account')

    @api.model
    def _create_account_move_line(self, line, move_id, credit_account_id,
                                  debit_account_id, qty_out,
                                  already_out_account_id):
        """
        Generate the account.move.line values to track the landed cost.
        Afterwards, for the goods that are already out of stock, we should
        create the out moves
        """
        aml_obj = self.env['account.move.line']
        base_line = {
            'name': line.name,
            'move_id': move_id,
            'product_id': line.product_id.id,
            'quantity': line.quantity,
            'credit': 0,
            'debit': 0
        }
        debit_line = dict(base_line, account_id=debit_account_id)
        credit_line = dict(
            base_line, account_id=credit_account_id,
            analytic_account_id=line.cost_line_id.analytic_id.id)
        diff = line.additional_landed_cost
        if diff > 0:
            debit_line['debit'] = diff
            credit_line['credit'] = diff
        else:
            # negative cost, reverse the entry
            debit_line['credit'] = -diff
            credit_line['debit'] = -diff
        aml_obj.create(debit_line)
        aml_obj.create(credit_line)
        # Create account move lines for quants already out of stock
        name = u'{}: {} {}'.format(line.name, qty_out, _(' already out'))
        if qty_out > 0:
            debit_line = dict(
                base_line, name=name, quantity=qty_out,
                account_id=already_out_account_id,
                analytic_account_id=line.cost_id.analytic_id.id)
            credit_line = dict(
                base_line, name=name, quantity=qty_out,
                account_id=debit_account_id)
            diff = diff * qty_out / line.quantity
            unit_debit = 0
            unit_credit = 0
            if diff > 0:
                debit_line['debit'] = diff
                credit_line['credit'] = diff
                unit_debit = diff / qty_out
            else:
                # negative cost, reverse the entry
                debit_line['credit'] = -diff
                credit_line['debit'] = -diff
                unit_credit = - diff / qty_out
            for quant in line.move_id.quant_ids.filtered(
                    lambda x: x.location_id.usage != 'internal'):
                aml_obj.create(dict(
                    debit_line, quantity=quant.qty,
                    credit=unit_credit * quant.qty,
                    debit=unit_debit * quant.qty,
                    partner_id=line.move_id.picking_id.partner_id.
                    commercial_partner_id.id))
            aml_obj.create(credit_line)

            # Ugly work-around to know if anglo-saxon accounting is used.
            # In 9.0, we can use the
            # field 'anglo_saxon_accounting' on the company.
            if hasattr(self.pool['account.invoice.line'],
                       '_anglo_saxon_sale_move_lines'):
                debit_line = dict(
                    base_line, name=name, quantity=qty_out,
                    account_id=credit_account_id,
                    analytic_account_id=line.cost_line_id.analytic_id.id,
                    debit=0, credit=0)
                credit_line = dict(
                    base_line, name=name, quantity=qty_out,
                    account_id=already_out_account_id,
                    analytic_account_id=line.cost_id.analytic_id.id,
                    debit=0, credit=0)
                unit_debit = 0
                unit_credit = 0
                if diff > 0:
                    debit_line['debit'] = diff
                    credit_line['credit'] = diff
                    unit_credit = diff / qty_out
                else:
                    # negative cost, reverse the entry
                    debit_line['credit'] = -diff
                    credit_line['debit'] = -diff
                    unit_debit = - diff / qty_out
                aml_obj.create(debit_line)
                for quant in line.move_id.quant_ids.filtered(
                        lambda x: x.location_id.usage != 'internal'):
                    aml_obj.create(
                        dict(credit_line, quantity=quant.qty,
                             credit=unit_credit * quant.qty,
                             debit=unit_debit * quant.qty,
                             partner_id=line.move_id.picking_id.partner_id.
                             commercial_partner_id.id))
        return True


class StockLandedCostLines(models.Model):

    _inherit = 'stock.landed.cost.lines'

    analytic_id = fields.Many2one(comodel_name='account.analytic.account',
                                  string='Analytic Account')
