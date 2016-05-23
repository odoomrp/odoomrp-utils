# -*- coding: utf-8 -*-
# (c) 2015 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import exceptions, fields, _


class TestSaleOrderManualClose(common.TransactionCase):

    def setUp(self):
        super(TestSaleOrderManualClose, self).setUp()
        self.sale_model = self.env['sale.order']
        self.finish_wk_model = self.env['wizard.saleorder.wf']
        uom_unit_id = self.ref('product.product_uom_unit')
        line1 = {'name': 'Laptop E5023',
                 'product_id': self.ref('product.product_product_25'),
                 'product_uom_qty': 3,
                 'product_uos_qty': 3,
                 'product_uom': uom_unit_id,
                 'price_unit': 2950.00
                 }
        line2 = {'name': 'Pen drive, 16GB',
                 'product_id': self.ref('product.product_product_30'),
                 'product_uom_qty': 5,
                 'product_uos_qty': 5,
                 'product_uom': uom_unit_id,
                 'price_unit': 145.00
                 }
        line3 = {'name': 'Headset USB',
                 'product_id': self.ref('product.product_product_33'),
                 'product_uom_qty': 2,
                 'product_uos_qty': 2,
                 'product_uom': uom_unit_id,
                 'price_unit': 65.00
                 }
        partner_id = self.ref('base.res_partner_2')
        sale_vals = {
            'partner_id': partner_id,
            'partner_invoice_id': partner_id,
            'partner_shipping_id': partner_id,
            'user_id': self.ref('base.user_demo'),
            'pricelist_id': self.ref('product.list0'),
            'section_id': self.ref('sales_team.section_sales_department'),
            'date_order': fields.Date.today(),
            'order_line': [(0, 0, line1), (0, 0, line2), (0, 0, line3)],
            'order_policy': 'manual'
        }
        self.order = self.sale_model.create(sale_vals)

    def test_draft_order_finish(self):
        try:
            self.finish_wk_model.with_context(
                active_model='sale.order', active_id=self.order.id,
                active_ids=[self.order.id]).saleorder_finish_wf()
        except exceptions.Warning as e:
            self.assertEqual(e.message, _("Cannot process already processed or"
                                          " in 'draft' state order."),
                             "The order is not in draft state.")

    def test_cancel_order_finish(self):
        self.order.signal_workflow('cancel')
        try:
            self.finish_wk_model.with_context(
                active_model='sale.order', active_id=self.order.id,
                active_ids=[self.order.id]).saleorder_finish_wf()
        except exceptions.Warning as e:
            self.assertEqual(e.message, _("Cannot process already processed or"
                                          " in 'draft' state order."),
                             "The order is not in cancel state.")

    def test_confirm_order_finish_error(self):
        self.order.action_button_confirm()
        try:
            self.finish_wk_model.with_context(
                active_model='sale.order', active_id=self.order.id,
                active_ids=[self.order.id]).saleorder_finish_wf()
        except exceptions.Warning as e:
            self.assertEqual(e.message,
                             _("The order has no processed picking."),
                             "All pickings are canceled or processed.")

    def test_confirm_order_picking_raise_finish(self):
        self.order.action_button_confirm()
        self.order.action_invoice_create()
        self.order.invoice_ids.signal_workflow('invoice_cancel')
        try:
            self.finish_wk_model.with_context(
                active_model='sale.order', active_id=self.order.id,
                active_ids=[self.order.id]).saleorder_finish_wf()
        except exceptions.Warning as e:
            self.assertEqual(e.message,
                             _("The order has no processed picking."),
                             "All pickings are canceled or processed.")

    def test_confirm_order_invoice_raise_finish(self):
        self.order.action_button_confirm()
        self.order.action_invoice_create()
        self.order.picking_ids.action_cancel()
        try:
            self.finish_wk_model.with_context(
                active_model='sale.order', active_id=self.order.id,
                active_ids=[self.order.id]).saleorder_finish_wf()
        except exceptions.Warning as e:
            self.assertEqual(e.message,
                             _("The order has no processed invoices."),
                             "All invoices are canceled or processed.")

    def test_confirm_order_ok_finish(self):
        self.order.action_button_confirm()
        self.order.action_invoice_create()
        self.order.invoice_ids.signal_workflow('invoice_cancel')
        self.order.picking_ids.action_cancel()
        self.finish_wk_model.with_context(
            active_model='sale.order', active_id=self.order.id,
            active_ids=[self.order.id]).saleorder_finish_wf()
        self.assertEqual(self.order.state, 'done',
                         "Orders workflow is not finished.")

    def test_order_already_processed_finish(self):
        self.order.action_button_confirm()
        self.order.action_invoice_create()
        self.order.invoice_ids.signal_workflow('invoice_cancel')
        self.order.picking_ids.action_cancel()
        self.finish_wk_model.with_context(
            active_model='sale.order', active_id=self.order.id,
            active_ids=[self.order.id]).saleorder_finish_wf()
        try:
            self.finish_wk_model.with_context(
                active_model='sale.order', active_id=self.order.id,
                active_ids=[self.order.id]).saleorder_finish_wf()
        except exceptions.Warning as e:
            self.assertEqual(e.message, _("Cannot process already processed or"
                                          " in 'draft' state order."),
                             "The order is not already processed.")
