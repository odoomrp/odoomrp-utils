# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestProductCost(common.TransactionCase):

    def setUp(self):
        super(TestProductCost, self).setUp()
        self.product = self.env.ref('product.product_product_6')

    def test_compute_average_manual_margin(self):
        average_margin = self.product.list_price - self.product.standard_price
        self.assertEqual(self.product.average_margin, average_margin,
                         'Average margin doesn\'t match')
        manual_margin = \
            self.product.list_price - self.product.manual_standard_cost
        self.assertEqual(self.product.manual_margin, manual_margin,
                         'Manual margin doesn\'t match')
