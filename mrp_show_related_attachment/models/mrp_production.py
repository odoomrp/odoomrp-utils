# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api


class MrpProduction(models.Model):

    _inherit = 'mrp.production'

    @api.one
    @api.depends('product_id')
    def _calc_production_attachments(self):
        self.product_attachments = None
        if self.product_id:
            cond = [('res_model', '=', 'product.product'),
                    ('res_id', '=', self.product_id.id)]
            attachments = self.env['ir.attachment'].search(cond)
            self.product_attachments = [(6, 0, attachments.mapped('id'))]

    product_attachments = fields.Many2many(
        comodel_name='ir.attachment',
        relation='rel_mrp_production_product_attachment',
        column1='production_id', column2='attachment_id', readonly=True,
        string='Product attachments', compute='_calc_production_attachments')


class MrpProductionWorkcenterLine(models.Model):

    _inherit = 'mrp.production.workcenter.line'

    @api.one
    @api.depends('workcenter_id')
    def _calc_workcenter_line_attachments(self):
        self.workcenter_attachments = None
        if self.workcenter_id:
            cond = [('res_model', '=', 'mrp.workcenter'),
                    ('res_id', '=', self.workcenter_id.id)]
            attachments = self.env['ir.attachment'].search(cond)
            self.workcenter_attachments = [(6, 0, attachments.mapped('id'))]

    workcenter_attachments = fields.Many2many(
        comodel_name='ir.attachment',
        relation='rel_workcenterline_workcenter_attachment',
        column1='workcenter_line_id', column2='attachment_id', readonly=True,
        string='Workcenter attachments',
        compute='_calc_workcenter_line_attachments')
