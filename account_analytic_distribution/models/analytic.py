# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api, exceptions, _


class AnalyticDistributionLine(models.Model):

    _name = 'analytic.distribution.line'

    analytic_id = fields.Many2one(comodel_name='account.analytic.account',
                                  string="Analytic Account",
                                  domain=[('type', '!=', 'view')])
    parent_id = fields.Many2one(comodel_name='account.analytic.account',
                                string="Parent")
    percent = fields.Integer(string="Percentage %")


class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    distribution_line_ids = fields.One2many(
        comodel_name='analytic.distribution.line', inverse_name='parent_id',
        string='Distribution Lines')
    distribution_type = fields.Selection(
        [('amount', 'Amount'), ('qty', 'Quantity')],
        string='Distribution Type')

    @api.constrains('distribution_line_ids')
    def _distribution_percentage_sum(self):
        if (self.distribution_line_ids and
                sum([x.percent for x in self.distribution_line_ids]) != 100):
            raise exceptions.Warning(
                _("Error! The sum of distribution lines percent is not 100."))

    def _get_child_accounts(self, account):
        accounts = self.env['account.analytic.account']
        for record in self:
            my_accounts = record.distribution_line_ids.mapped('analytic_id')
            accounts |= my_accounts
            if account.id in accounts.ids:
                return accounts
            for my_account in my_accounts:
                accounts |= my_account._get_child_accounts(account=account)
        return accounts

    @api.constrains('distribution_line_ids')
    def check_recursion(self):
        if self.id in self._get_child_accounts(account=self).ids:
            raise exceptions.Warning(_("Error! There is recursion between this"
                                       " account and distribution lines."))


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    @api.multi
    def needs_distribution(self, account):
        return bool(self.env['account.analytic.account'].browse(
            account).distribution_line_ids)

    @api.multi
    def load_distribution_data(self, account, type, percent, amount, qty):
        load_amount = amount
        load_qty = qty
        if type == 'amount':
            load_amount = amount * percent / 100
        elif type == 'qty':
            load_qty = qty * percent / 100
        self.write({'account_id': account.id,
                    'amount': load_amount,
                    'unit_amount': load_qty})

    @api.multi
    def make_distribution(self):
        for line in self:
            type = line.account_id.distribution_type
            amount = line.amount
            qty = line.unit_amount
            distribution_lines = line.account_id.distribution_line_ids
            distribution_line = distribution_lines[0]
            line.load_distribution_data(distribution_line.analytic_id, type,
                                        distribution_line.percent, amount, qty)
            for distribution_line in distribution_lines[1:]:
                new_line = line.copy()
                new_line.load_distribution_data(
                    distribution_line.analytic_id, type,
                    distribution_line.percent, amount, qty)

    @api.multi
    def write(self, vals):
        res = super(AccountAnalyticLine, self).write(vals)
        if (vals.get('account_id', False) and
                self.needs_distribution(vals.get('account_id'))):
            self.make_distribution()
        return res

    @api.model
    def create(self, vals):
        res = super(AccountAnalyticLine, self).create(vals)
        if (vals.get('account_id', False) and
                self.needs_distribution(vals.get('account_id'))):
            res.make_distribution()
        return res
