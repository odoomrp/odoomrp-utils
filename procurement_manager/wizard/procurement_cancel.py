# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, api


class ProcurementCancel(models.TransientModel):
    _name = 'procurement.cancel'
    _description = "Cancel the selected procurements"

    @api.one
    def cancel_procurements(self):
        active_ids = self.env.context.get('active_ids', [])
        cond = [('id', 'in', active_ids),
                ('state', 'in', ('exception', 'confirmed', 'running'))]
        procurements = self.env['procurement.order'].search(cond)
        procurements.cancel()
        return True
