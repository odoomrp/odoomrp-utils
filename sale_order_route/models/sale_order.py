# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    route_id = fields.Many2one(comodel_name='stock.location.route',
                               string='Route',
                               domain=[('sale_selectable', '=', True)])

    @api.multi
    @api.onchange('route_id')
    def onchange_route_id(self):
        self.ensure_one()
        for line in self.order_line:
            line.route_id = self.route_id
