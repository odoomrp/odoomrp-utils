# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import exceptions, fields


class TestAccountAnalyticDistribution(common.TransactionCase):

    def setUp(self):
        super(TestAccountAnalyticDistribution, self).setUp()
        self.analytic_model = self.env['account.analytic.account']
        self.distribution_line_model = self.env['analytic.distribution.line']
        self.analytic_line_model = self.env['account.analytic.line']
        self.account = self.ref('account.a_recv')
        self.journal = self.ref('account.analytic_journal_sale')
        self.analytic_1 = self.analytic_model.create(
            {'name': 'Test Account 1', 'type': 'normal',
             'distribution_type': 'amount'})
        self.analytic_2 = self.analytic_model.create(
            {'name': 'Test Account 2', 'type': 'normal',
             'distribution_type': 'amount'})
        self.analytic_3 = self.analytic_model.create(
            {'name': 'Test Account 3', 'type': 'normal',
             'distribution_type': 'amount'})
        self.analytic_4 = self.analytic_model.create(
            {'name': 'Test Account 2', 'type': 'normal',
             'distribution_type': 'amount'})
        self.analytic_5 = self.analytic_model.create(
            {'name': 'Test Account 2', 'type': 'normal',
             'distribution_type': 'amount'})
        self.distribution_1 = self.distribution_line_model.create(
            {'analytic_id': self.analytic_2.id, 'percent': 75,
             'parent_id': self.analytic_1.id})
        self.distribution_2 = self.distribution_line_model.create(
            {'analytic_id': self.analytic_3.id, 'percent': 25,
             'parent_id': self.analytic_1.id})

    def test_constraint_percent_sum(self):
        self.distribution_1.percent = 80
        with self.assertRaises(exceptions.Warning):
            self.analytic_1._distribution_percentage_sum()

    def test_constraint_recursion(self):
        self.distribution_line_model.create(
            {'analytic_id': self.analytic_1.id, 'percent': 100,
             'parent_id': self.analytic_2.id})
        with self.assertRaises(exceptions.Warning):
            self.analytic_1.check_recursion()

    def test_analytic_line_create_by_amount(self):
        analytic_line_vals = {
            'account_id': self.analytic_1.id,
            'general_account_id': self.account,
            'journal_id': self.journal,
            'amount': 50,
            'unit_amount': 1,
            'date': fields.Date.today(),
            'name': 'Test Analytic Line'}
        analytic_line = self.analytic_line_model.create(analytic_line_vals)
        self.assertEqual(analytic_line.account_id.id, self.analytic_2.id,
                         "The distribution account is not correct.")
        self.assertEqual(analytic_line.amount, 37.5,
                         "The distribution amount is not correct.")
        cond = [('name', '=', 'Test Analytic Line'), ('amount', '=', 12.5),
                ('account_id', '=', self.analytic_3.id)]
        line = self.analytic_line_model.search(cond)
        self.assertEqual(len(line), 1, "The distribution is not correct.")

    def test_analytic_line_create_by_qty(self):
        self.analytic_1.distribution_type = 'qty'
        analytic_line_vals = {
            'account_id': self.analytic_1.id,
            'general_account_id': self.account,
            'journal_id': self.journal,
            'amount': 50,
            'unit_amount': 4,
            'date': fields.Date.today(),
            'name': 'Test Analytic Line'}
        analytic_line = self.analytic_line_model.create(analytic_line_vals)
        self.assertEqual(analytic_line.account_id.id, self.analytic_2.id,
                         "The distribution account is not correct.")
        self.assertEqual(analytic_line.unit_amount, 3,
                         "The distribution amount is not correct.")
        cond = [('name', '=', 'Test Analytic Line'), ('unit_amount', '=', 1),
                ('account_id', '=', self.analytic_3.id)]
        line = self.analytic_line_model.search(cond)
        self.assertEqual(len(line), 1, "The distribution is not correct.")

    def test_analytic_line_write(self):
        analytic_line_vals = {
            'account_id': self.analytic_3.id,
            'general_account_id': self.account,
            'journal_id': self.journal,
            'amount': 50,
            'unit_amount': 4,
            'date': fields.Date.today(),
            'name': 'Test Analytic Line'}
        analytic_line = self.analytic_line_model.create(analytic_line_vals)
        analytic_line.write({'account_id': self.analytic_1.id})
        self.assertEqual(analytic_line.account_id.id, self.analytic_2.id,
                         "The distribution account is not correct.")
        self.assertEqual(analytic_line.amount, 37.5,
                         "The distribution amount is not correct.")
        cond = [('name', '=', 'Test Analytic Line'), ('amount', '=', 12.5),
                ('account_id', '=', self.analytic_3.id)]
        line = self.analytic_line_model.search(cond)
        self.assertEqual(len(line), 1, "The distribution is not correct.")

    def test_recursive_distribution(self):
        self.distribution_line_model.create(
            {'analytic_id': self.analytic_4.id, 'percent': 50,
             'parent_id': self.analytic_3.id})
        self.distribution_line_model.create(
            {'analytic_id': self.analytic_5.id, 'percent': 50,
             'parent_id': self.analytic_3.id})
        analytic_line_vals = {
            'account_id': self.analytic_1.id,
            'general_account_id': self.account,
            'journal_id': self.journal,
            'amount': 100,
            'unit_amount': 4,
            'date': fields.Date.today(),
            'name': 'Test Analytic Line'}
        self.analytic_line_model.create(analytic_line_vals)
        cond = [('name', '=', 'Test Analytic Line'), ('amount', '=', 75),
                ('account_id', '=', self.analytic_2.id)]
        line = self.analytic_line_model.search(cond)
        self.assertEqual(len(line), 1, "The distribution is not correct.")
        cond = [('name', '=', 'Test Analytic Line'), ('amount', '=', 25),
                ('account_id', '=', self.analytic_3.id)]
        line = self.analytic_line_model.search(cond)
        self.assertEqual(len(line), 0, "The distribution is not correct.")
        cond = [('name', '=', 'Test Analytic Line'), ('amount', '=', 12.5),
                ('account_id', '=', self.analytic_4.id)]
        line = self.analytic_line_model.search(cond)
        self.assertEqual(len(line), 1, "The distribution is not correct.")
        cond = [('name', '=', 'Test Analytic Line'), ('amount', '=', 12.5),
                ('account_id', '=', self.analytic_5.id)]
        line = self.analytic_line_model.search(cond)
        self.assertEqual(len(line), 1, "The distribution is not correct.")
