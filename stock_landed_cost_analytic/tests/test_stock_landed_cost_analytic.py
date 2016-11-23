# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestStockLandedCostAnalytic(common.TransactionCase):

    def setUp(self):
        super(TestStockLandedCostAnalytic, self).setUp()
        self.picking_type_model = self.env['stock.picking.type']
        self.picking_model = self.env['stock.picking']
        self.stock_move_model = self.env['stock.move']
        self.analytic_model = self.env['account.analytic.account']
        self.landed_cost_model = self.env['stock.landed.cost']
        self.landed_cost_line_model = self.env['stock.landed.cost.lines']
        self.account_move_line_model = self.env['account.move.line']
        self.partner = self.ref('base.res_partner_2')
        self.product = self.env.ref('product.product_product_4')
        self.input_account = self.ref('account.stk')
        self.output_account = self.ref('account.ova')
        self.product.write(
            {'cost_method': 'real',
             'valuation': 'real_time',
             'property_stock_account_input': self.input_account,
             'property_stock_account_output': self.output_account})
        picking_type = self.picking_type_model.search(
            [('code', '=', 'outgoing')], limit=1)
        self.picking = self.picking_model.create({
            'partner_id': self.partner,
            'picking_type_id': picking_type[:1].id,
            'invoice_state': '2binvoiced'
        })
        self.picking_move = self.stock_move_model.create({
            'name': self.product.name,
            'picking_id': self.picking.id,
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 15,
            'location_id': picking_type[:1].default_location_src_id.id,
            'location_dest_id': (picking_type[:1].default_location_dest_id.id),
        })
        self.picking.action_done()
        account_journal = self.env.ref('stock_account.stock_journal')
        analytic_journal = self.env['account.analytic.journal'].create({
            'code': 'STK',
            'name': 'Stock Journal',
            'type': 'general'
            })
        account_journal.analytic_journal_id = analytic_journal
        self.incoming_analytic_id = self.analytic_model.create({
            'name': 'INCOMING',
            'type': 'normal'
            })
        self.outgoing_analytic_id = self.analytic_model.create({
            'name': 'OUTGOING',
            'type': 'normal'
            })
        self.landed_cost = self.landed_cost_model.create({
            'picking_ids': [(6, 0, [self.picking.id])],
            'account_journal_id': account_journal.id,
            'analytic_id': self.outgoing_analytic_id.id
        })
        self.landed_cost_line = self.landed_cost_line_model.create({
            'name': 'Test Line',
            'cost_id': self.landed_cost.id,
            'product_id': self.ref('product.product_product_1'),
            'price_unit': 300,
            'split_method': 'equal',
            'account_id': self.ref('account.a_expense'),
            'analytic_id': self.incoming_analytic_id.id
        })

    def test_landed_cost_validation_split_by_quant(self):
        self.landed_cost.compute_landed_cost()
        self.landed_cost.button_validate()
        account_move_lines = self.account_move_line_model.search(
            [('account_id', '=', self.output_account),
             ('analytic_account_id', '=', self.outgoing_analytic_id.id),
             ('move_id', '=', self.landed_cost.account_move_id.id)])
        self.assertEqual(len(account_move_lines), len(
            self.picking_move.quant_ids.filtered(
                lambda x: x.location_id.usage != 'internal')),
            'Account move lines no splited by quant.')

    def test_landed_cost_validation_set_analytic_account(self):
        self.landed_cost.compute_landed_cost()
        self.landed_cost.button_validate()
        for line in self.landed_cost.cost_lines:
            account_move_lines = self.account_move_line_model.search(
                [('account_id', '=', line.account_id.id),
                 ('analytic_account_id', '=', line.analytic_id.id),
                 ('move_id', '=', self.landed_cost.account_move_id.id)])
            self.assertNotEqual(len(account_move_lines), 0,
                                'Incoming analytic account wrong.')

    def test_import_invoice_lines(self):
        landed_lines_count = len(self.landed_cost.cost_lines)
        invoice_lines = [
            self.ref('account.demo_invoice_0_line_rpanrearpanelshe0'),
            self.ref('account.demo_invoice_0_line_rckrackcm0')]
        self.env['landed.cost.import.invoice.lines'].with_context(
            active_id=self.landed_cost.id).create(
                {'invoice_line_ids': [(6, 0, invoice_lines)]}).import_lines()
        self.assertEqual(len(self.landed_cost.cost_lines),
                         landed_lines_count + 2,
                         'Invoice line not correctly imported.')

    def test_landed_cost_negative_aditional_value(self):
        self.landed_cost_line.price_unit = -300
        self.landed_cost.compute_landed_cost()
        self.landed_cost.button_validate()
        account_move_lines = self.account_move_line_model.search(
            [('account_id', '=', self.landed_cost_line.account_id.id),
             ('analytic_account_id', '=',
              self.landed_cost_line.analytic_id.id),
             ('move_id', '=', self.landed_cost.account_move_id.id)])
        self.assertNotEqual(len(account_move_lines), 0,
                            'Incoming analytic account wrong.')
