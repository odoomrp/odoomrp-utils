# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, api


class ProcurementRun(models.TransientModel):
    _name = 'procurement.run'
    _description = "Run the selected procurements"

    @api.one
    def run_procurements(self):
        procurement_obj = self.env['procurement.order']
        active_ids = self.env.context.get('active_ids', [])
        for procurement in procurement_obj.browse(active_ids).filtered(
                lambda x: x.state in ('confirmed', 'exception')):
            procurement.run()
            cond = [('id', 'not in', active_ids),
                    ('product_id', '=', procurement.product_id.id),
                    ('warehouse_id', '=', procurement.warehouse_id.id),
                    ('location_id', '=', procurement.location_id.id),
                    ('rule_id', '=', procurement.rule_id.id),
                    ('state', '=', procurement.state)]
            procurements = procurement_obj.search(cond)
            procurements.run()
        return True
