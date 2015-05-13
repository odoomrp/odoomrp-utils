# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    claim_count = fields.Integer(
        string='Claim Count', compute='_count_claim')

    @api.one
    def _count_claim(self):
        claim_obj = self.env['crm.claim']
        search_term = '%s,%i' % (self._model, self.id)
        claims = claim_obj.search([('ref', '=', search_term)])
        self.claim_count = len(claims)

    @api.multi
    def action_open_claims(self):
        template_obj = self.env['product.template']
        claim_obj = self.env['crm.claim']
        search_term = '%s,%i' % (self._model, self.id)
        claims = claim_obj.search([('ref', '=', search_term)])
        result = template_obj._get_act_window_dict(
            'crm_claim.crm_case_categ_claim0')
        result['domain'] = "[('id', 'in', " + str(claims.ids) + ")]"
        return result
