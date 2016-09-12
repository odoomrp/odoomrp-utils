# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.multi
    def do_unreserve(self):
        res = super(StockMove, self).do_unreserve()
        self.mapped('raw_material_production_id').signal_workflow(
            'button_not_ready')
        return res
