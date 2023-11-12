# -*- coding: utf-8 -*-

from odoo import models, fields


class ClassRoom(models.Model):
    _inherit = 'ems.class.room'

    timetable__ids = fields.One2many('ems.timetable','class_id')
    

    def action_open_timetable(self):
        for rec in self:
            return {
                'name': 'Timetable',
                'type': 'ir.actions.act_window',
                'res_model': 'ems.timetable',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', rec.timetable__ids.ids)],
            }
        
