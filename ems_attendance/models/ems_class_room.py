# -*- coding: utf-8 -*-

from odoo import models, fields


class ClassRoom(models.Model):
    _inherit = 'ems.class.room'

    attendance_ids = fields.One2many('ems.attendance','class_id')


    def action_open_attendance(self):
        for rec in self:
            return {
                'name': 'Attendance',
                'type': 'ir.actions.act_window',
                'res_model': 'ems.attendance',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', rec.attendance_ids.ids )],
            }
        
