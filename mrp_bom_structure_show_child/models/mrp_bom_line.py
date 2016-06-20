# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    @api.multi
    def _compute_standard_price(self):
        for record in self:
            template_std_price = record.product_uom._compute_price(
                record.product_id.uom_id.id, record.product_id.standard_price,
                record.product_uom.id)
            if not record.product_id:
                try:
                    template_std_price =\
                        record.product_uom._compute_price(
                            record.product_tmpl_id.uom_id.id,
                            record.product_tmpl_id.standard_price,
                            record.product_uom.id)
                except AttributeError:
                    # This is in case mrp_product_variants module is not
                    # installed
                    template_std_price = 0.0
            record.standard_price = template_std_price

    @api.multi
    def _compute_childs_standard_price(self):
        for record in self:
            childs_standard_price = 0.0
            for line in record.child_line_ids:
                childs_standard_price += (
                    (line.product_qty / line.bom_id.product_qty) *
                    (line.standard_price + line.childs_standard_price))
            record.childs_standard_price = childs_standard_price

    @api.multi
    def _compute_child_bom_id(self):
        for record in self:
            record.child_bom_id = record.child_line_ids[:1].bom_id

    routing_id = fields.Many2one(
        comodel_name='mrp.routing', string="Productive Process",
        related="bom_id.routing_id", store=True, readonly=True)
    standard_price = fields.Float(
        string='Cost Price', compute='_compute_standard_price',
        digits=dp.get_precision('Product Price'))
    childs_standard_price = fields.Float(
        string='Childs Cost Price', compute='_compute_childs_standard_price',
        digits=dp.get_precision('Product Price'))
    child_bom_id = fields.Many2one(
        comodel_name='mrp.bom', compute='_compute_child_bom_id')
    bom_qty = fields.Float(related='child_bom_id.product_qty')
