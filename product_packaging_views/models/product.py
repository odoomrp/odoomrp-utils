# -*- coding: utf-8 -*-
# Copyright 2014-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2014-2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3

from openerp import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    packagings = fields.One2many(
        comodel_name='product.packaging', inverse_name='product_tmpl_id',
        string='Packagings',
    )
