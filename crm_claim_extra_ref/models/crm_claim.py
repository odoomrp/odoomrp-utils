# -*- coding: utf-8 -*-
# Copyright 2015 AvanzOsc (http://www.avanzosc.es)
# Copyright 2015-2016 - Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from openerp import api, fields, models


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    @api.multi
    def _links_get(self):
        link_obj = self.env['res.request.link']
        return [(r.object, r.name) for r in link_obj.search([])]

    @api.multi
    @api.depends('ref2')
    def _compute_ref_model_name2(self):
        model_obj = self.env['ir.model']
        for claim in self:
            claim.ref_model_name2 = False
            if claim.ref2:
                cond = [('model', '=', str(claim.ref2._model))]
                model = model_obj.search(cond)
                claim.ref_model_name2 = model.name

    @api.multi
    @api.depends('ref2')
    def _compute_ref_name2(self):
        for claim in self:
            claim.ref_name2 = False
            if claim.ref2:
                claim.ref_name2 = claim.ref2.name_get()[0][1]

    @api.multi
    @api.depends('ref3')
    def _compute_ref_model_name3(self):
        model_obj = self.env['ir.model']
        for claim in self:
            claim.ref_model_name3 = False
            if claim.ref3:
                cond = [('model', '=', str(claim.ref3._model))]
                model = model_obj.search(cond)
                claim.ref_model_name3 = model.name

    @api.multi
    @api.depends('ref3')
    def _compute_ref_name3(self):
        for claim in self:
            claim.ref_name3 = False
            if claim.ref3:
                claim.ref_name3 = claim.ref3.name_get()[0][1]

    ref2 = fields.Reference(string='Reference 2', selection=_links_get)
    ref_model_name2 = fields.Char(
        string='Ref. Model 2', compute='_compute_ref_model_name2', store=True,
    )
    ref_name2 = fields.Char(
        string='Ref. Name 2', compute='_compute_ref_name2', store=True,
    )
    ref3 = fields.Reference(string='Reference 3', selection=_links_get)
    ref_model_name3 = fields.Char(
        string='Ref. Model 3', compute='_compute_ref_model_name3', store=True,
    )
    ref_name3 = fields.Char(
        string='Ref. Name 3', compute='_compute_ref_name3', store=True,
    )
