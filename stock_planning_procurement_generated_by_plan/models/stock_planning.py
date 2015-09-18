# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class StockPlanning(models.Model):
    _inherit = 'stock.planning'

    @api.one
    def _get_to_date(self):
        super(StockPlanning, self)._get_to_date()
        proc_obj = self.env['procurement.order']
        states = ('confirmed', 'exception')
        procurements = proc_obj._find_procurements_from_stock_planning(
            self.company, self.scheduled_date, self.from_date, states,
            product=self.product, warehouse=self.warehouse,
            location_id=self.location)
        procurements = procurements.filtered(
            lambda x: x.level > 0)
        self.procurement_plan_incoming_to_date = sum(
            x.product_qty for x in procurements)
        if self.scheduled_to_date and self.procurement_plan_incoming_to_date:
            self.scheduled_to_date -= self.procurement_plan_incoming_to_date

    procurement_plan_incoming_to_date = fields.Float(
        'Incoming up to date from procurements plan', compute='_get_to_date',
        digits_compute=dp.get_precision('Product Unit of Measure'))
