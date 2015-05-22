# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.multi
    def action_open_quants(self):
        template_obj = self.env['product.template']
        products = self.env['product.product']
        if self.state in ['in_production', 'done']:
            lines = self.move_lines
        else:
            lines = self.product_lines
        for line in lines:
            products |= line.product_id
        result = template_obj._get_act_window_dict('stock.product_open_quants')
        result['domain'] = "[('product_id', 'in', " + str(products.ids) + ")]"
        result['context'] = {'search_default_productgroup': 1,
                             'search_default_internal_loc': 1}
        return result
