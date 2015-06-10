# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api, _
from dateutil.relativedelta import relativedelta


class WizStockPlanning(models.TransientModel):

    _name = 'wiz.stock.planning'
    _description = 'Wiz Stock Planning'

    @api.multi
    def _def_company(self):
        return self.env.user.company_id.id

    company = fields.Many2one('res.company', 'Company', default=_def_company,
                              required=True)
    scheduled_date = fields.Date('Scheduled date', required=True)
    days = fields.Integer('Days interval', required=True)
    to_date = fields.Date('To date', required=True)

    @api.multi
    def calculate_stock_planning(self):
        self.ensure_one()
        move_obj = self.env['stock.move']
        procurement_obj = self.env['procurement.order']
        planning_obj = self.env['stock.planning']
        planning = planning_obj.search([])
        planning.unlink()
        fdate = self.scheduled_date
        from_date = False
        while fdate < self.to_date:
            product_datas = {}
            cond = [('company_id', '=', self.company.id),
                    ('date', '<=', fdate),
                    ('state', 'not in', ('done', 'cancel'))]
            if from_date:
                cond.append(('date', '>', from_date))
            moves = move_obj.search(cond)
            for move in moves:
                if move.location_id.usage == 'internal':
                    product_datas = self._find_product_in_table(
                        product_datas, move.product_id, move.location_id,
                        move.warehouse_id)
                if move.location_dest_id.usage == 'internal':
                    product_datas = self._find_product_in_table(
                        product_datas, move.product_id,
                        move.location_dest_id, move.warehouse_id)
            cond = [('company_id', '=', self.company.id),
                    ('date_planned', '<=', fdate),
                    ('state', 'in', ('confirmed', 'running'))]
            if from_date:
                cond.append(('date_planned', '>', from_date))
            procurements = procurement_obj.search(cond)
            for procurement in procurements:
                if procurement.location_id.usage == 'internal':
                    product_datas = self._find_product_in_table(
                        product_datas, procurement.product_id,
                        procurement.location_id, procurement.warehouse_id)
            for data in product_datas:
                datos_array = product_datas[data]
                vals = {'company': self.company.id,
                        'location': datos_array['location'].id,
                        'from_date': from_date,
                        'scheduled_date': fdate,
                        'product': datos_array['product'].id}
                if datos_array['warehouse']:
                    vals['warehouse'] = datos_array['warehouse'].id
                else:
                    cond = [('company_id', '=', self.company.id),
                            ('lot_stock_id', '=', datos_array['location'].id)]
                    warehouses = self.env['stock.warehouse'].search(cond)
                    if warehouses:
                        vals['warehouse'] = warehouses[0].id
                planning_obj.create(vals)
            from_date = fdate
            fdate = fields.Date.to_string(fields.Date.from_string(fdate) +
                                          relativedelta(days=self.days))
        return {'name': _('Stock Planning'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'stock.planning',
                }

    def _find_product_in_table(self, product_datas, product, location,
                               warehouse):
        found = False
        for data in product_datas:
            datos_array = product_datas[data]
            dproduct = datos_array['product']
            dlocation = datos_array['location']
            dwarehouse = datos_array['warehouse']
            if dproduct.id == product.id and dlocation.id == location.id:
                found = True
                if not dwarehouse and warehouse:
                    product_datas[data].update({'warehouse': warehouse})
                break
        if not found:
            my_vals = {'product': product,
                       'location': location,
                       'warehouse': warehouse,
                       }
            ind = product.id + location.id + (warehouse.id or 0)
            product_datas[(ind)] = my_vals
        return product_datas
