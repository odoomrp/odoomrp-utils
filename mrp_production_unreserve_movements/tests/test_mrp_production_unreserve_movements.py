# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestMrpProductionUnreserveMovements(common.TransactionCase):

    def setUp(self):
        super(TestMrpProductionUnreserveMovements, self).setUp()
        self.production = self.env.ref(
            'mrp_operations_extension.mrp_production_opeext')
        self.production.signal_workflow('button_confirm')
        self.production.force_production()

    def test_unreserve_workcenter_lines(self):
        wk_line = self.production.workcenter_lines[:1]
        assigned_lines = wk_line.move_lines.filtered(lambda x: x.state ==
                                                     'assigned')
        self.assertTrue(assigned_lines, 'There is no stock for products.')
        self.assertTrue(wk_line.show_unreserve)
        self.assertFalse(wk_line.show_force_reservation)
        self.assertFalse(wk_line.show_check_availability)
        wk_line.button_unreserve()
        assigned_lines = wk_line.move_lines.filtered(lambda x: x.state ==
                                                     'assigned')
        self.assertFalse(assigned_lines, 'There are some moves assigned.')
        self.assertFalse(wk_line.show_unreserve)
        self.assertTrue(wk_line.show_force_reservation)
        self.assertTrue(wk_line.show_check_availability)

    def test_unreserve_production(self):
        assigned_lines = self.production.move_lines.filtered(
            lambda x: x.state == 'assigned')
        self.assertTrue(assigned_lines, 'There is no stock for products.')
        self.assertEqual(self.production.state, 'ready')
        self.assertTrue(self.production.show_unreserve)
        self.assertFalse(self.production.show_force_reservation)
        self.assertFalse(self.production.show_check_availability)
        self.production.button_unreserve()
        assigned_lines = self.production.move_lines.filtered(
            lambda x: x.state == 'assigned')
        self.assertFalse(assigned_lines, 'There are some moves assigned.')
        self.assertEqual(self.production.state, 'confirmed')
        self.assertFalse(self.production.show_unreserve)
        self.assertTrue(self.production.show_force_reservation)
        self.assertTrue(self.production.show_check_availability)
