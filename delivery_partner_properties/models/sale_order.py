# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    property_mandatory_carrier = fields.Many2one(
        comodel_name='delivery.carrier', string='Mandatory delivery method',
        related='partner_id.property_mandatory_carrier')

    @api.multi
    def onchange_partner_id(self, partner_id):
        res = super(SaleOrder, self).onchange_partner_id(partner_id)
        res['value'].update({'carrier_id': False})
        partner = self.env['res.partner'].browse(partner_id)
        if partner.property_mandatory_carrier:
            res['value'].update(
                {'carrier_id': partner.property_mandatory_carrier.id})
        if partner.banned_carrier_ids:
            res.update({'domain':
                        {'carrier_id':
                         [('id', 'not in', partner.banned_carrier_ids.ids)]}})
        else:
            res.update({'domain': {'carrier_id': []}})
        return res

    @api.model
    def create(self, vals):
        partner = self.env['res.partner'].browse(vals['partner_id'])
        if partner.property_mandatory_carrier:
            vals['carrier_id'] = partner.property_mandatory_carrier.id
        return super(SaleOrder, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('partner_id'):
            partner = self.env['res.partner'].browse(vals['partner_id'])
            if partner.property_mandatory_carrier:
                vals['carrier_id'] = partner.property_mandatory_carrier.id
        return super(SaleOrder, self).write(vals)
