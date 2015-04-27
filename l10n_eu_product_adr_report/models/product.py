# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields


class ProductAdrClass(models.Model):
    _name = 'product.adr.class'

    name = fields.Char(string='Name', size=64, required=True)
    picking_text = fields.Text(string='Description text in stock picking',
                               size=256, required=True, translate=True)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    adr_class_id = fields.Many2one(comodel_name='product.adr.class',
                                   string='Product ADR Class')
