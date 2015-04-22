# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, api


class ProcurementResetToConfirmed(models.TransientModel):
    _name = 'procurement.reset.to.confirmed'
    _description = "Reset to confirmed selected procurements"

    @api.one
    def reset_to_confirmed_procurements(self):
        active_ids = self.env.context.get('active_ids', [])
        cond = [('id', 'in', active_ids),
                ('state', '=', 'cancel')]
        procurements = self.env['procurement.order'].search(cond)
        procurements.reset_to_confirmed()
        return True
