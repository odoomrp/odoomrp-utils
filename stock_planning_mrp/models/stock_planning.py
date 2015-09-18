# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


class StockPlanning(models.Model):

    _inherit = 'stock.planning'

    @api.one
    def _get_to_date(self):
        production_obj = self.env['mrp.production']
        proc_obj = self.env['procurement.order']
        super(StockPlanning, self)._get_to_date()
        states = ('confirmed', 'exception')
        procurements = proc_obj._find_procurements_from_stock_planning(
            self.company, self.scheduled_date, self.from_date, states,
            product=self.product, warehouse=self.warehouse,
            location_id=self.location, without_purchases=True,
            without_productions=True)
        self.procurement_incoming_to_date = sum(x.product_qty for x in
                                                procurements)
        productions = production_obj._find_productions_from_stock_planning(
            self.company, self.scheduled_date, self.from_date, self.product,
            self.warehouse, self.location)
        self.incoming_in_mo = sum(x.product_qty for x in productions)
        mrp_productions = self.env['mrp.production']
        for line in productions:
            mrp_productions |= line
        self.productions = [(6, 0, mrp_productions.ids)]
        if self.from_date:
            cond = [('company', '=', self.company.id),
                    ('warehouse', '=', self.warehouse.id or False),
                    ('location', '=', self.location.id),
                    ('scheduled_date', '<', self.scheduled_date),
                    ('product', '=', self.product.id)]
            lines = self.search(cond)
            if lines:
                line = max(lines, key=lambda x: x.scheduled_date)
                self.incoming_in_mo += line.incoming_in_mo
        self.scheduled_to_date += self.incoming_in_mo

    incoming_in_mo = fields.Float(
        'Incoming in MO', compute='_get_to_date',
        digits_compute=dp.get_precision('Product Unit of Measure'))
    productions = fields.Many2many(
        comodel_name='mrp.production',
        relation='rel_stock_planning_mrp_production',
        column1='stock_planning_id', column2='production_id',
        string='MRP Productions', compute='_get_to_date')

    @api.multi
    def show_productions(self):
        self.ensure_one()
        return {'name': _('MRP Productions'),
                'view_type': 'form',
                "view_mode": 'tree,form',
                'res_model': 'mrp.production',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', self.productions.ids)]
                }
