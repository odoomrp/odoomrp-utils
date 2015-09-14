# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


class StockPlanning(models.Model):

    _inherit = 'stock.planning'

    def _calculate_incoming_in_mo(self):
        production_obj = self.env['mrp.production']
        cond = [('company_id', '=', self.company.id),
                ('product_id', '=', self.product.id),
                ('date_planned', '<=', self.scheduled_date),
                ('state', '=', 'draft')]
        if self.from_date:
            cond.append(('date_planned', '>', self.from_date))
        if self.location:
            cond.append(('location_dest_id', '=', self.location.id))
        productions = production_obj.search(cond)
        return productions

    @api.one
    def _get_to_date(self):
        super(StockPlanning, self)._get_to_date()
        productions = self._calculate_incoming_in_mo()
        self.incoming_in_mo = sum(productions.mapped('product_qty'))
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
