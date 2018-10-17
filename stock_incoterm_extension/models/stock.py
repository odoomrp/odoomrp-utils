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


class StockIncoterms(models.Model):

    _inherit = 'stock.incoterms'

    destination_port = fields.Boolean(string="Requires destination port")
    transport_type = fields.Boolean(string="Requires transport type")
    default_destination_port = fields.Char(string="Default Destination Port")


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.model
    def _get_selection_transport_type(self):
        return self.env['sale.order'].fields_get(
            allfields=['transport_type'])['transport_type']['selection']

    incoterm = fields.Many2one('stock.incoterms', string="Incoterm")
    req_destination_port = fields.Boolean(string="Requires destination port",
                                          related="incoterm.destination_port")
    req_transport_type = fields.Boolean(string="Requires transport type",
                                        related="incoterm.transport_type")
    destination_port = fields.Char(string="Destination port")
    transport_type = fields.Selection(
        selection='_get_selection_transport_type', string="Transport type")

    @api.onchange('incoterm')
    def _onchange_incoterm(self):
        for picking in self:
            picking.destination_port = (
                picking.incoterm.default_destination_port)

    @api.model
    def _create_invoice_from_picking(self, picking, vals):
        if picking:
            vals.update({
                'incoterm': picking.incoterm and picking.incoterm.id or False,
                'destination_port': picking.destination_port,
                'transport_type': picking.transport_type,
            })
        return super(StockPicking, self)._create_invoice_from_picking(
            picking, vals)


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def _prepare_picking_assign(self, move):
        """ Prepares a new picking for this move as it could not be assigned to
        another picking. This method is designed to be inherited.
        """
        values = super(StockMove, self)._prepare_picking_assign(move=move)
        if (move.procurement_id and move.procurement_id.sale_line_id):
            sale = move.procurement_id.sale_line_id.order_id
            values.update({
                'incoterm': sale.incoterm.id,
                'destination_port': sale.destination_port,
                'transport_type': sale.transport_type,
            })
        return values
