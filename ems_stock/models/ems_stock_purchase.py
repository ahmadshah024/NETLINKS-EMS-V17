# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError




class EmsStockPurchase(models.Model):
    _name = 'ems.stock.purchase'
    _description = 'ems stock purchase description'
 


    name = fields.Char()
    date = fields.Date("Date")
    amount=fields.Float("Amount")
    product_id=fields.Many2one('product.template')

    line_ids=fields.One2many("ems.stock.purchase.line","purchase_id")
    # sales_id = fields.Many2one('atlas.sale')


    @api.constrains('line_ids')
    def _total_bill(self):
        if any(self.line_ids):
            total = 0
            for line in self.line_ids:
                total = total + line.total
            self.amount = total
        elif not any(self.line_ids):
            raise ValidationError("Sorry! you have not enterded any item to purchase")
        self.write({"state":"approved"})

    state = fields.Selection([('draft', 'Draft'),('approved', 'Approved')], default='draft', help='Choose whether the investment is still approved or not')
    
    def action_draft(self):
        for rec in self:
            rec.state = 'draft'


    def action_approved(self):
        for line in self.line_ids:
            current_onhand = line.product_id.on_hand_quantity
            line.product_id.write({'on_hand_quantity': current_onhand + line.quantity})
        self.write({'state': 'approved'})


class EmsStockProductLine(models.Model):
    _name = 'ems.stock.purchase.line'
    _description = 'ems stock product line description'


    quantity = fields.Integer("Quantity")
    price = fields.Float("Price")
    total = fields.Float(string='Total', compute='_total_amount')

    product_id=fields.Many2one('product.template')
    purchase_id=fields.Many2one('ems.stock.purchase')


    @api.depends('quantity','price')
    def _total_amount(self):
            for line in self:
                line.total = line.quantity * line.price
