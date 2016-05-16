# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, tools


class AnalyticProductionCostReport(models.Model):
    _name = "analytic.production.cost.report"
    _description = "Analytic Production Cost Report"
    _auto = False

    date = fields.Date('Date', readonly=True)
    user_id = fields.Many2one('res.users', string='User', readonly=True)
    name = fields.Char(string='Description', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    company_id = fields.Many2one(
        'res.company', string='Company', required=True)
    currency_id = fields.Many2one(
        'res.currency', string='Currency', required=True)
    account_id = fields.Many2one(
        'account.analytic.account', string='Account', required=True)
    general_account_id = fields.Many2one(
        'account.account', string='General Account', required=True)
    journal_id = fields.Many2one(
        'account.analytic.journal', string='Journal', required=True)
    move_id = fields.Many2one(
        'account.move.line', string='Move', required=True)
    product_id = fields.Many2one(
        'product.product', string='Product', required=True)
    product_uom_id = fields.Many2one(
        'product.uom', string='Product Unit of Measure', required=True)
    production = fields.Many2one(
        'mrp.production', string='Production', readonly=True)
    workorder = fields.Many2one(
        'mrp.production.workcenter.line', string='Work order', readonly=True)
    amount = fields.Float(string='amount', readonly=True)
    unit_amount = fields.Integer(string='Unit Amount', readonly=True)
    nbr = fields.Integer(string='# Entries', readonly=True)

    def _select(self):
        select_str = """
        SELECT  min(a.id) as id, count(distinct a.id) as nbr, a.date as date,
           a.user_id as user_id, a.name as name,  a.company_id as company_id,
           analytic.partner_id as partner_id, a.currency_id as currency_id,
           a.account_id as account_id, a.journal_id as journal_id,
           a.general_account_id as general_account_id, a.move_id as move_id,
           a.product_id as product_id, a.product_uom_id as product_uom_id,
           a.mrp_production_id as production, a.workorder as workorder,
           sum(a.amount) as amount, sum(a.unit_amount) as unit_amount
        """
        return select_str

    def _from(self):
        from_str = """
        FROM account_analytic_line a inner join
             account_analytic_account analytic on a.account_id = analytic.id
        """
        return from_str

    def _group_by(self):
        group_by_str = """
        GROUP BY  a.date, a.user_id, a.name, analytic.partner_id, a.company_id,
            a.currency_id, a.account_id, a.general_account_id, a.journal_id,
            a.move_id, a.product_id, a.product_uom_id, a.mrp_production_id,
            a.workorder
        """
        return group_by_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (%s %s %s)
        """ % (self._table, self._select(), self._from(), self._group_by()))
