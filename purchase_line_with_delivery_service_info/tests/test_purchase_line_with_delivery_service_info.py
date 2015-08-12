# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
import openerp.tests.common as common


class TestPurchaseLineWithDeliveryServiceInfo(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseLineWithDeliveryServiceInfo, self).setUp()
        self.route_model = self.env['stock.location.route']
        self.product_model = self.env['product.product']
        self.sale_model = self.env['sale.order']
        self.sale_line_model = self.env['sale.order.line']
        self.procurement_model = self.env['procurement.order']
        routes = self.route_model.search(
            [('name', 'in', ('Make To Order', 'Buy'))])
        self.assertEqual(len(routes), 2,
                         "Make to order, and buy routes not found")
        vals = self.sale_model.onchange_partner_id(
            self.env.ref('base.res_partner_1').id).get('value')
        line = self.sale_line_model.product_id_change(
            pricelist=vals.get('pricelist_id'),
            product=self.env.ref('product.product_product_6').id, qty=1,
            qty_uos=1,
            partner_id=self.env.ref('base.res_partner_1').id).get('value')
        line['product_id'] = self.env.ref('product.product_product_6').id
        vals.update({'partner_id': self.env.ref('base.res_partner_1').id,
                     'order_line': [(0, 0, line)],
                     'carrier_id':
                     self.env.ref('delivery.normal_delivery_carrier').id})
        self.new_sale_order = self.sale_model.create(vals)
        self.new_sale_order.delivery_set()
        for line in self.new_sale_order.order_line:
            if line.product_id.type == 'service':
                line.product_id.write(
                    {'route_ids': [(6, 0, routes.mapped('id'))],
                     'seller_ids':
                     [(6, 0, [self.env.ref('base.res_partner_14').id])]})
                line.write({'delivery_standard_price': 578.00})

    def test_confirm_sale_with_delivery_service(self):
        self.new_sale_order.action_button_confirm()
        for line in self.new_sale_order.order_line:
            if line.product_id.type == 'service':
                cond = [('sale_line_id', '=', line.id)]
                procurement = self.procurement_model.search(cond)
                self.assertEqual(
                    len(procurement), 1,
                    "Procurement not generated for the service product type")
                procurement.run()
                cond = [('id', '>', procurement.id),
                        ('sale_line_id', '=', line.id)]
                procurement2 = self.procurement_model.search(cond)
                self.assertEqual(
                    len(procurement2), 1,
                    "Procurement2 not generated for the service product type")
                procurement2.run()
                self.assertTrue(
                    bool(procurement2.purchase_id),
                    "Purchase no generated for procurement Service")
                for line in procurement2.purchase_id.order_line:
                    if line.product_id.type == 'service':
                        self.assertEqual(
                            line.price_unit,
                            procurement2.sale_line_id.delivery_standard_price,
                            "Erroneous price on purchase order line")
