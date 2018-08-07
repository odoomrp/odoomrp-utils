# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    @api.model
    def _get_selection_transport_type(self):
        return self.env['sale.order'].fields_get(
            allfields=['transport_type'])['transport_type']['selection']

    req_destination_port = fields.Boolean(
        string="Requires destination port",
        related="incoterm_id.destination_port")
    req_transport_type = fields.Boolean(
        string="Requires transport type",
        related="incoterm_id.transport_type")
    destination_port = fields.Char(string="Destination port")
    transport_type = fields.Selection(
        selection='_get_selection_transport_type', string="Transport type")

    @api.onchange('incoterm_id')
    def _onchange_incoterm(self):
        for order in self:
            order.destination_port = order.incoterm_id.default_destination_port

    @api.model
    def _prepare_invoice(self, order, line_ids):
        res = super(PurchaseOrder, self)._prepare_invoice(order, line_ids)
        res.update({
            'incoterm': order.incoterm_id.id,
            'destination_port': order.destination_port,
            'transport_type': order.transport_type
            })
        return res
