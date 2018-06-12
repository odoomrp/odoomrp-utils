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

from openerp import models, fields


class PricelistPartnerinfo(models.Model):
    _inherit = 'pricelist.partnerinfo'

    partner = fields.Many2one(
        comodel_name='res.partner', string='Partner',
        related='suppinfo_id.name', store=True)
    type = fields.Selection(
        string='Type', related='suppinfo_id.type', store=True)
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template', string='Product Template',
        related='suppinfo_id.product_tmpl_id', store=True)
    product_name = fields.Char(
        string='Product Name', related='suppinfo_id.product_name', store=True)
    product_code = fields.Char(
        string='Product Code', related='suppinfo_id.product_code', store=True)
    sequence = fields.Integer(
        string='Sequence', related='suppinfo_id.sequence', store=True)
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company',
        related='suppinfo_id.company_id', store=True)
