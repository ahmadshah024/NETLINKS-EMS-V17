# -*- coding: utf-8 -*-

from odoo import models, fields


class ClassRoom(models.Model):
    _inherit = 'ems.class.room'

    teacher_ids = fields.One2many('hr.employee','class_id')


    def action_open_teacher(self):
        for rec in self:
            return {
                'name': 'Teacher',
                'type': 'ir.actions.act_window',
                'res_model': 'hr.employee',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', rec.teacher_ids.ids )],
            }
        
