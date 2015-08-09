# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    @api.multi
    def _links_get(self):
        link_obj = self.env['res.request.link']
        return [(r.object, r.name) for r in link_obj.search([])]

    @api.one
    @api.depends('ref2')
    def _generate_ref_model_name2(self):
        model_obj = self.env['ir.model']
        self.ref_model_name2 = False
        if self.ref2:
            cond = [('model', '=', str(self.ref2._model))]
            model = model_obj.search(cond)
            self.ref_model_name2 = model.name

    @api.one
    @api.depends('ref2')
    def _generate_ref_name2(self):
        self.ref_name2 = False
        if self.ref2:
            self.ref_name2 = self.ref2.name_get()[0][1]

    @api.one
    @api.depends('ref3')
    def _generate_ref_model_name3(self):
        model_obj = self.env['ir.model']
        self.ref_model_name3 = False
        if self.ref3:
            cond = [('model', '=', str(self.ref3._model))]
            model = model_obj.search(cond)
            self.ref_model_name3 = model.name

    @api.one
    @api.depends('ref3')
    def _generate_ref_name3(self):
        self.ref_name3 = False
        if self.ref3:
            self.ref_name3 = self.ref3.name_get()[0][1]

    ref2 = fields.Reference(string='Reference 2', selection=_links_get)
    ref_model_name2 = fields.Char(
        string='Ref. Model 2', compute='_generate_ref_model_name2', store=True)
    ref_name2 = fields.Char(
        string='Ref. Name 2', compute='_generate_ref_name2', store=True)
    ref3 = fields.Reference(string='Reference 3', selection=_links_get)
    ref_model_name3 = fields.Char(
        string='Ref. Model 3', compute='_generate_ref_model_name3', store=True)
    ref_name3 = fields.Char(
        string='Ref. Name 3', compute='_generate_ref_name3', store=True)
