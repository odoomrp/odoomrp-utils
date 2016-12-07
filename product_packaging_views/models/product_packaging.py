# -*- coding: utf-8 -*-
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3

from openerp import models, fields


class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    def _default_ul(self):
        return self.env['product.ul'].search([], limit=1).id

    ul = fields.Many2one(
        comodel_name='product.ul', string='Package Logistic Unit',
        required=True, default=_default_ul,
    )
    ul_qty = fields.Integer(
        string='Package by layer', help='The number of packages by layer',
    )
    ul_container = fields.Many2one(
        comodel_name='product.ul', string='Pallet Logistic Unit',
    )
    rows = fields.Integer(
        string='Number of Layers', required=True, default=3,
        help='The number of layers on a pallet or box',
    )
