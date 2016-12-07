# -*- coding: utf-8 -*-
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3

from openerp import fields, models


class ProductUl(models.Model):
    _name = "product.ul"
    _description = "Logistic Unit"

    name = fields.Char(
        string='Name', index=True, required=True, translate=True,
    )
    type = fields.Selection(
        selection=[
            ('unit', 'Unit'),
            ('pack', 'Pack'),
            ('box', 'Box'),
            ('pallet', 'Pallet'),
        ], string='Type', required=True,
    )
    height = fields.Float(string='Height', help='The height of the package')
    width = fields.Float(string='Width', help='The width of the package')
    ul_length = fields.Float(
        string='Length', help='The length of the package', oldname='length',
    )
    weight = fields.Float(string='Empty Package Weight')
    packagings = fields.One2many(
        comodel_name='product.packaging', inverse_name='ul_container',
        string='Packagings',
    )
    product = fields.Many2one(
        comodel_name='product.product', string='Product',
        help='This is the related product when the UL is sold.',
    )
    ul_qty = fields.Float(string='Quantity')
