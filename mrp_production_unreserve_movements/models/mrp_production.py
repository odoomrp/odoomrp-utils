# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.depends('state', 'move_lines.state')
    def _show_buttons(self):
        for mo in self.filtered(lambda x: x.state not in
                                ('draft', 'cancel', 'done')):
            moves = mo.move_lines.filtered(
                lambda x: x.state in ('waiting', 'confirmed') and
                x.work_order.state not in ('cancel', 'done'))
            mo.show_check_availability = moves
            mo.show_force_reservation = moves

    @api.depends('move_lines.state')
    def _show_unreserve(self):
        for mo in self:
            mo.show_unreserve = mo.move_lines.filtered(
                lambda x: x.state == 'assigned' and
                x.work_order.state not in ('cancel', 'done'))

    show_check_availability = fields.Boolean(
        string='Show check availability button', compute='_show_buttons')
    show_force_reservation = fields.Boolean(
        string='Show force reservation button', compute='_show_buttons')
    show_unreserve = fields.Boolean(
        string='Show unreserve button', compute='_show_unreserve')

    @api.multi
    def button_unreserve(self):
        moves = self.move_lines.filtered(
            lambda x: x.state == 'assigned' and (
                not x.work_order or x.work_order.state == 'draft'))
        return moves.do_unreserve()

    @api.multi
    def check_unreserved_moves(self):
        self.ensure_one()
        moves = self.move_lines.filtered(
            lambda x: x.state in ('assigned', 'done'))
        if moves:
            return False
        return True

    @api.multi
    def action_confirm(self):
        mo_to_confirm = self.filtered(lambda x: not x.product_lines or
                                      not x.move_lines)
        mo_no_confirm = self.filtered(lambda x: x.product_lines and
                                      x.move_lines)
        mo_no_confirm.write({'state': 'confirmed'})
        return super(MrpProduction, mo_to_confirm).action_confirm()


class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.production.workcenter.line'

    @api.one
    @api.depends('state', 'production_id.move_lines.state')
    def _show_buttons(self):
        self.show_check_availability = False
        self.show_force_reservation = False
        if self.state not in ('cancel', 'done'):
            moves = self.production_id.move_lines.filtered(
                lambda x: x.state in ('waiting', 'confirmed') and
                x.work_order.id == self.id)
            if moves:
                self.show_check_availability = True
                self.show_force_reservation = True

    @api.one
    @api.depends('production_id.move_lines.state')
    def _show_unreserve(self):
        self.show_unreserve = False
        if self.state not in ('cancel', 'done'):
            moves = self.production_id.move_lines.filtered(
                lambda x: x.state == 'assigned' and
                x.work_order.id == self.id)
            if moves:
                self.show_unreserve = True

    show_check_availability = fields.Boolean(
        string='Show check availability button', compute='_show_buttons')
    show_force_reservation = fields.Boolean(
        string='Show force reservation button', compute='_show_buttons')
    show_unreserve = fields.Boolean(
        string='Show unreserve button', compute='_show_unreserve')

    @api.multi
    def button_unreserve(self):
        moves = self.production_id.move_lines.filtered(
            lambda x: x.state == 'assigned' and
            x.work_order.id == self.id)
        return moves.do_unreserve()
