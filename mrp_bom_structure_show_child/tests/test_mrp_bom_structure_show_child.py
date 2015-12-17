# -*- coding: utf-8 -*-
# (c) 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests.common import TransactionCase


class TestMrpBomStructureShowChild(TransactionCase):

    def setUp(self):
        super(TestMrpBomStructureShowChild, self).setUp()
        self.bom = self.env.ref('mrp.mrp_bom_2')

    def test_computed_childs_standard_price(self):
        for bom_line in self.bom.bom_line_ids:
            childs_standard_price = 0.0
            for line in bom_line.child_line_ids:
                childs_standard_price += (
                    (line.product_qty / line.bom_id.product_qty) *
                    (line.standard_price + line.childs_standard_price))
            self.assertEquals(
                bom_line.childs_standard_price, childs_standard_price)

    def test_computed_template_standard_price(self):
        for bom_line in self.bom.bom_line_ids:
            price = 15.0
            bom_line.product_id.standard_price = price
            if not bom_line.product_id:
                try:
                    bom_line.product_template.standard_price = price
                except AttributeError:
                    # This is in case mrp_product_variants module is not
                    # installed
                    price = 0.0
            self.assertEquals(
                bom_line.standard_price, price, "Prices do not match.")

    def test_computed_child_bom_id(self):
        for bom_line in self.bom.bom_line_ids:
            self.assertEquals(
                bom_line.child_bom_id, bom_line.child_line_ids[:1].bom_id)
