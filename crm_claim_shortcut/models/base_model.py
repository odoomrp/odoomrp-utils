# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import fields, api, _
from openerp.models import BaseModel
from lxml import etree


base_fields_view_get = BaseModel.fields_view_get


def new_fields_view_get(
        self, cr, uid, view_id=None, view_type='form', context=None,
        toolbar=False, submenu=False):
    res = base_fields_view_get(
        self, cr, uid, view_id=view_id, view_type=view_type, context=context,
        toolbar=toolbar, submenu=submenu)
    view = self.pool['ir.ui.view'].browse(cr, uid, view_id, context=context)
    has_model = self.pool['res.request.link'].search(
        cr, uid, [('object', '=', view.model)], context=context)
    if view_type == 'form' and has_model:
        eview = etree.fromstring(res['arch'])

        def _check_rec(eview):
            if 'oe_button_box' in eview.attrib.get('class', ''):
                new_field = etree.Element(
                    'field', {'string': _('Claims'),
                              'name': 'claim_count',
                              'widget': 'statinfo'})
                new_button = etree.Element(
                    'button', {'class': 'oe_inline oe_stat_button',
                               'type': 'object',
                               'name': 'action_open_claims',
                               'icon': 'fa-comments',
                               'groups': 'base.group_sale_salesman',
                               'context': ("{'search_default_partner_id': "
                                           "active_id, 'default_partner_id': "
                                           "active_id}")})
                new_button.append(new_field)
                eview.append(new_button)

            for child in eview:
                _check_rec(child)
            return True

        _check_rec(eview)
        res['arch'] = etree.tostring(eview)
    return res


@api.one
def _open_related_claims(self):
    claim_obj = self.env['crm.claim']
    act_window_obj = self.env['ir.actions.act_window']
    search_term = '%s,%i' % (self._model, self.id)
    claims = claim_obj.search([('ref', '=', search_term)])
    result = act_window_obj.for_xml_id('crm_claim', 'crm_case_categ_claim0')
    result['domain'] = "[('id', 'in', " + str(claims.ids) + ")]"
    return result

crm_claim_count = fields.Integer(
    string='Claim Count', compute='_count_claim')


@api.one
def _count_claim(self):
    claim_obj = self.env['crm.claim']
    search_term = '%s,%i' % (self._model, self.id)
    claims = claim_obj.search([('ref', '=', search_term)])
    self.crm_claim_count = len(claims)


BaseModel.action_open_claims = _open_related_claims
BaseModel.fields_view_get = new_fields_view_get
