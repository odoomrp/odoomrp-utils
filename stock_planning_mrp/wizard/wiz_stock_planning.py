# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api
from dateutil.relativedelta import relativedelta


class WizStockPlanning(models.TransientModel):

    _inherit = 'wiz.stock.planning'

    @api.multi
    def _def_company(self):
        return self.env.user.company_id.id

    company = fields.Many2one(
        'res.company', 'Company', default=_def_company, required=True)
    from_date = fields.Date(
        'From date', required=True,
        default=lambda self: fields.Date.context_today(self),
        help='Date from which the interval starts counting days')
    days = fields.Integer(
        'Days interval', required=True,
        help='Increase number of days starting from the date from')
    to_date = fields.Date('To date', required=True,
                          help='Deadline for calculating periods')
    category = fields.Many2one(
        'product.category', 'Category',
        help='Enter this field if you want to filter by category')
    template = fields.Many2one(
        'product.template', 'Template',
        help='Enter this field if you want to filter by template')
    product = fields.Many2one(
        'product.product', 'Product',
        help='Enter this field if you want to filter by product')

    @api.multi
    def calculate_stock_planning(self):
        warehouse_obj = self.env['stock.warehouse']
        self.ensure_one()
        result = super(WizStockPlanning, self).calculate_stock_planning()
        fdate = self.from_date
        from_date = False
        product_datas = {}
        while fdate < self.to_date:
            for production in self._find_productions(fdate, from_date):
                cond = [('company_id', '=', self.company.id),
                        ('lot_stock_id', '=', production.location_dest_id.id)]
                warehouse = warehouse_obj.search(cond, limit=1)
                product_datas = self._find_product_in_table(
                    product_datas, production.product_id,
                    production.location_dest_id, warehouse or False)
            from_date = fdate
            fdate = fields.Date.to_string(fields.Date.from_string(fdate) +
                                          relativedelta(days=self.days))
        self._generate_stock_planning_from_productions(product_datas)
        return result

    def _find_productions(self, fdate, from_date):
        production_obj = self.env['mrp.production']
        cond = [('company_id', '=', self.company.id),
                ('date_planned', '<=', fdate),
                ('state', '=', 'draft')]
        if from_date:
            cond.append(('date_planned', '>', from_date))
        if self.product:
            cond.append(('product_id', '=', self.product.id))
        productions = production_obj.search(cond).filtered(
            lambda x: x.location_dest_id.usage == 'internal')
        return productions

    def _generate_stock_planning_from_productions(self, product_datas):
        planning_obj = self.env['stock.planning']
        for data in product_datas:
            datos_array = product_datas[data]
            fdate = self.from_date
            from_date = False
            while fdate < self.to_date:
                cond = [('company', '=', self.company.id),
                        ('location', '=', datos_array['location'].id),
                        ('scheduled_date', '=', fdate),
                        ('product', '=', datos_array['product'].id)]
                if from_date:
                    cond.append(('from_date', '=', from_date))
                if datos_array['warehouse']:
                    cond.append(('warehouse', '=',
                                 datos_array['warehouse'].id))
                else:
                    cond = [('company_id', '=', self.company.id),
                            ('lot_stock_id', '=', datos_array['location'].id)]
                    warehouses = self.env['stock.warehouse'].search(cond)
                    if warehouses:
                        cond.append(('warehouse', '=', warehouses[0].id))
                planning = planning_obj.search(cond, limit=1)
                if not planning:
                    vals = {'company': self.company.id,
                            'location': datos_array['location'].id,
                            'scheduled_date': fdate,
                            'product': datos_array['product'].id}
                    if from_date:
                        vals['from_date'] = from_date
                    if datos_array['warehouse']:
                        vals['warehouse'] = datos_array['warehouse'].id
                    else:
                        cond = [('company_id', '=', self.company.id),
                                ('lot_stock_id', '=',
                                 datos_array['location'].id)]
                        warehouses = self.env['stock.warehouse'].search(cond)
                        if warehouses:
                            vals['warehouse'] = warehouses[0].id
                    planning_obj.create(vals)
                from_date = fdate
                fdate = fields.Date.to_string(fields.Date.from_string(fdate) +
                                              relativedelta(days=self.days))
