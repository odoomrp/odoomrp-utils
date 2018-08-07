# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common


class TestStockIncotermExtension(common.TransactionCase):

    def setUp(self):
        super(TestStockIncotermExtension, self).setUp()
        self.invoice_model = self.env['account.invoice']
        self.journal = self.env.ref('account.sales_journal')
        self.sale_order = self.env.ref('sale.sale_order_2')
        self.sale_order1 = self.env.ref('sale.sale_order_1')
        self.purchase_order = self.env.ref('purchase.purchase_order_1')
        self.incoterm = self.env.ref('stock.incoterm_EXW')
        self.incoterm.destination_port = False
        self.incoterm.transport_type = True
        self.incoterm.default_destination_port = 'port1'
        self.sale_order.incoterm = self.incoterm
        self.sale_order.transport_type = 'air'
        self.sale_order1.incoterm = self.incoterm
        self.sale_order1.transport_type = 'ground'
        self.purchase_order.incoterm_id = self.incoterm
        self.purchase_order.transport_type = 'maritime'

    def test_sale_order_invoice(self):
        self.sale_order.order_policy = 'manual'
        self.sale_order.action_button_confirm()
        res = self.sale_order.manual_invoice()
        inv_id = res.get('res_id', False)
        invoice = self.invoice_model.browse(inv_id)
        self.assertTrue(invoice and invoice.incoterm.id == self.incoterm.id and
                        invoice.transport_type == 'air')
        self.assertFalse(invoice.destination_port)
        invoice._onchange_incoterm()

    def test_purchase_order_invoice(self):
        self.purchase_order.signal_workflow('purchase_confirm')
        invoice = self.purchase_order.invoice_ids and \
            self.purchase_order.invoice_ids[0]
        self.assertFalse(invoice and invoice.destination_port)
        self.assertTrue(invoice and invoice.incoterm.id == self.incoterm.id and
                        invoice.transport_type == 'maritime')

    def test_sale_order_picking_invoice(self):
        self.sale_order1.order_policy = 'picking'
        self.sale_order1.action_button_confirm()
        pickings = self.sale_order1.picking_ids
        self.assertFalse(pickings.destination_port)
        pickings._onchange_incoterm()
        self.assertEquals(pickings.destination_port,
                          self.incoterm.default_destination_port)
        invoice_ids = pickings.action_invoice_create(
            journal_id=self.journal.id)
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertTrue(invoices and invoices[0].incoterm.id ==
                        self.incoterm.id and invoices[0].transport_type ==
                        'ground' and invoices[0].destination_port == 'port1')

    def test_sale_order_onchange(self):
        self.assertTrue(self.incoterm.default_destination_port)
        self.sale_order._onchange_incoterm()
        self.assertEquals(self.sale_order.destination_port,
                          self.incoterm.default_destination_port)

    def test_purchase_order_onchange(self):
        self.assertTrue(self.incoterm.default_destination_port)
        self.purchase_order._onchange_incoterm()
        self.assertEquals(self.purchase_order.destination_port,
                          self.incoterm.default_destination_port)
