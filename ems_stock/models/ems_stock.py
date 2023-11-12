# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsStock(models.Model):
    _inherit = 'product.template'


    is_uniform = fields.Boolean()
    is_book = fields.Boolean()
    price = fields.Integer()


    on_hand_quantity = fields.Integer(readonly=True)


    purchase_ids = fields.One2many('ems.stock.purchase', 'product_id')
    purchase_count = fields.Integer(string='Number of Returns', compute='_compute_purchase_count')

    @api.depends('purchase_ids')
    def _compute_purchase_count(self):
        for product in self:
            product.purchase_count = len(product.purchase_ids)

    def action_show_purchases(self):
        for rec in self:
            return {
                'name': 'Purchase',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'res_model': 'ems.stock.purchase',
                'domain': [('id', 'in', rec.purchase_ids.line_ids.ids)],
            }