# -*- coding: utf-8 -*-
# (c) 2015 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import exceptions, fields


class TestPurchaseOrderManualClose(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseOrderManualClose, self).setUp()
        self.purchase_model = self.env['purchase.order']
        self.finish_wk_model = self.env['purchase.order.finish.wf']
        uom_unit_id = self.ref('product.product_uom_unit')
        line1 = {'name': 'Laptop E5023',
                 'product_id': self.ref('product.product_product_25'),
                 'product_qty': 3,
                 'product_uom': uom_unit_id,
                 'price_unit': 2950.00,
                 'date_planned': fields.Date.today(),
                 }
        line2 = {'name': 'Pen drive, 16GB',
                 'product_id': self.ref('product.product_product_30'),
                 'product_qty': 5,
                 'product_uom': uom_unit_id,
                 'price_unit': 145.00,
                 'date_planned': fields.Date.today(),
                 }
        line3 = {'name': 'Headset USB',
                 'product_id': self.ref('product.product_product_33'),
                 'product_qty': 2,
                 'product_uom': uom_unit_id,
                 'price_unit': 65.00,
                 'date_planned': fields.Date.today(),
                 }
        partner = self.env.ref('base.res_partner_2')
        picking_type = self.env['stock.picking.type'].browse(
            self.purchase_model._get_picking_in())
        purchase_vals = {
            'partner_id': partner.id,
            'pricelist_id': partner.property_product_pricelist_purchase.id,
            'date_order': fields.Date.today(),
            'order_line': [(0, 0, line1), (0, 0, line2), (0, 0, line3)],
            'invoice_method': 'order',
            'company_id': self.env['res.company']._company_default_get(
                'purchase.order'),
            'picking_type_id': picking_type.id,
            'location_id': picking_type.default_location_dest_id.id,
        }
        self.order = self.purchase_model.create(purchase_vals)

    def test_draft_order_finish(self):
        try:
            self.finish_wk_model.with_context(
                active_model='purchase.order', active_id=self.order.id,
                active_ids=[self.order.id], lang='en_US').end_workflow()
        except exceptions.Warning as e:
            self.assertEqual(e.message, "Cannot process already processed or"
                             " in 'draft' state order.",
                             "The order is not in draft state.")

    def test_cancel_order_finish(self):
        self.order.signal_workflow('cancel')
        try:
            self.finish_wk_model.with_context(
                active_model='purchase.order', active_id=self.order.id,
                active_ids=[self.order.id], lang='en_US').end_workflow()
        except exceptions.Warning as e:
            self.assertEqual(e.message, "Cannot process already processed or"
                             " in 'draft' state order.",
                             "The order is not in cancel state.")

    def test_confirm_order_finish_error(self):
        self.order.signal_workflow('purchase_confirm')
        try:
            self.finish_wk_model.with_context(
                active_model='purchase.order', active_id=self.order.id,
                active_ids=[self.order.id], lang='en_US').end_workflow()
        except exceptions.Warning as e:
            self.assertEqual(e.message,
                             "The order has no processed picking.",
                             "All pickings are canceled or processed.")

    def test_confirm_order_picking_raise_finish(self):
        self.order.signal_workflow('purchase_confirm')
        self.order.invoice_ids.signal_workflow('invoice_cancel')
        try:
            self.finish_wk_model.with_context(
                active_model='purchase.order', active_id=self.order.id,
                active_ids=[self.order.id], lang='en_US').end_workflow()
        except exceptions.Warning as e:
            self.assertEqual(e.message,
                             "The order has no processed picking.",
                             "All pickings are canceled or processed.")

    def test_confirm_order_invoice_raise_finish(self):
        self.order.signal_workflow('purchase_confirm')
        self.order.picking_ids.action_cancel()
        try:
            self.finish_wk_model.with_context(
                active_model='sale.order', active_id=self.order.id,
                active_ids=[self.order.id], lang='en_US').end_workflow()
        except exceptions.Warning as e:
            self.assertEqual(e.message,
                             "The order has no processed invoices.",
                             "All invoices are canceled or processed.")

    def test_confirm_order_ok_finish(self):
        self.order.signal_workflow('purchase_confirm')
        self.order.invoice_ids.signal_workflow('invoice_cancel')
        self.order.picking_ids.action_cancel()
        self.finish_wk_model.with_context(
            active_model='purchase.order', active_id=self.order.id,
            active_ids=[self.order.id]).end_workflow()
        self.assertEqual(self.order.state, 'done',
                         "Orders workflow is not finished.")

    def test_order_already_processed_finish(self):
        self.order.signal_workflow('purchase_confirm')
        self.order.invoice_ids.signal_workflow('invoice_cancel')
        self.order.picking_ids.action_cancel()
        self.finish_wk_model.with_context(
            active_model='purchase.order', active_id=self.order.id,
            active_ids=[self.order.id]).end_workflow()
        try:
            self.finish_wk_model.with_context(
                active_model='purchase.order', active_id=self.order.id,
                active_ids=[self.order.id], lang='en_US').end_workflow()
        except exceptions.Warning as e:
            self.assertEqual(e.message, "Cannot process already processed or"
                             " in 'draft' state order.",
                             "The order is not already processed.")
