# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
import openerp.tests.common as common


class TestAccountInvoiceLineStockMoveInfo(common.TransactionCase):

    def setUp(self):
        super(TestAccountInvoiceLineStockMoveInfo, self).setUp()
        self.product_model = self.env['product.product']
        self.partner_model = self.env['res.partner']
        self.sale_model = self.env['sale.order']
        self.sale_line_model = self.env['sale.order.line']
        self.picking_model = self.env['stock.picking']
        self.transfer_details_model = self.env['stock.transfer_details']
        self.stock_invoice_model = self.env['stock.invoice.onshipping']
        self.invoice_line_model = self.env['account.invoice.line']
        product_vals = {
            'name': 'Product for stock move info',
            'standard_price': 20.5,
            'list_price': 30.75,
            'type': 'product'}
        self.product = self.product_model.create(product_vals)
        partner_vals = {'name': 'Customer for stock move info',
                        'customer': True}
        self.partner = self.partner_model.create(partner_vals)
        sale_vals = {'partner_id': self.partner.id,
                     'partner_shipping_id': self.partner.id,
                     'partner_invoice_id': self.partner.id,
                     'pricelist_id': self.env.ref('product.list0').id,
                     'order_policy': 'picking'}
        sale_line_vals = {'product_id': self.product.id,
                          'name': self.product.name,
                          'product_uos_qty': 1,
                          'product_uom': self.product.uom_id.id,
                          'price_unit': self.product.list_price}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.sale_model.create(sale_vals)

    def test_confirm_sale_and_generate_invoice(self):
        self.sale_order.action_button_confirm()
        pickings = self.picking_model.search([])
        # "Filtered" is used because the "sale_id" field of pickings is not
        # stored to disk
        picking = pickings.filtered(lambda x: x.sale_id == self.sale_order)
        self.assertEqual(len(picking), 1, "Picking not found")
        picking.force_assign()
        self.assertEqual(picking.state, 'assigned', "Picking not assigned")
        vals = {'picking_id': picking.id}
        transfer_details = self.transfer_details_model.with_context(
            active_ids=[picking.id], active_model='stock.picking').create(vals)
        transfer_details.do_detailed_transfer()
        self.assertEqual(picking.state, 'done', "Picking not in done state")
        picking.write({'invoice_state': '2binvoiced'})
        stock_invoice = self.stock_invoice_model.with_context(
            active_ids=[picking.id]).create({})
        stock_invoice.with_context(active_ids=[picking.id]).open_invoice()
        self.assertEqual(picking.invoice_state, 'invoiced',
                         "Picking not invoiced")
        for line in picking.move_lines:
            cond = [('move', '=', line.id)]
            invoice_line = self.invoice_line_model.search(cond, limit=1)
            self.assertEqual(len(invoice_line), 1, "Invoice line not found")
            invoice_line.invoice_id.action_cancel()
        self.assertEqual(picking.invoice_state, '2binvoiced',
                         "Picking invoice_state not in 2binvoiced")
