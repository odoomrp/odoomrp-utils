# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    req_destination_port = fields.Boolean(string="Requires destination port",
                                          related="incoterm.destination_port")
    req_transport_type = fields.Boolean(string="Requires transport type",
                                        related="incoterm.transport_type")
    destination_port = fields.Char(string="Destination port")
    transport_type = fields.Selection(
        selection=[('air', 'Air'), ('maritime', 'Maritime'),
                   ('ground', 'Ground')], string="Transport type")

    @api.onchange('incoterm')
    def _onchange_incoterm(self):
        for order in self:
            order.destination_port = order.incoterm.default_destination_port

    @api.model
    def _prepare_invoice(self, order, line_ids):
        res = super(SaleOrder, self)._prepare_invoice(order, line_ids)
        res.update({
            'incoterm': order.incoterm.id,
            'destination_port': order.destination_port,
            'transport_type': order.transport_type
            })
        return res
