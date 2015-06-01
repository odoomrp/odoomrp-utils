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

from openerp import models, fields


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    incoterm = fields.Many2one('stock.incoterms', string="Incoterm")
    req_destination_port = fields.Boolean(string="Requires destination port",
                                          related="incoterm.destination_port")
    req_transport_type = fields.Boolean(string="Requires transport type",
                                        related="incoterm.transport_type")
    destination_port = fields.Char(string="Destination port")
    transport_type = fields.Selection([('air', 'Air'),
                                       ('maritime', 'Maritime'),
                                       ('ground', 'Ground')],
                                      string="Transport type")
