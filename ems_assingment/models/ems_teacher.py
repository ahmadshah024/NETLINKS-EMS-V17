# -*- coding: utf-8 -*-

from odoo import models, fields


class EmsTeacher(models.Model):
    _inherit = 'hr.employee'


    assignment_ids = fields.One2many('ems.assignment','teacher_id')
    assignment_count = fields.Integer(compute='_compute_assignment_count')

    def _compute_assignment_count(self):
        for rec in self:
            rec.assignment_count = len(rec.assignment_ids)

    def action_open_assignment(self):
        for rec in self:
            return {
                'name': 'Active Assignments',
                'type': 'ir.actions.act_window',
                'res_model': 'ems.assignment',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', rec.assignment_ids.ids)],
            }
    def action_create_assignment(self):
            return {
                'name': 'Create Assignments',
                'type': 'ir.actions.act_window',
                'res_model': 'ems.assignment',
                'view_mode': 'form',
                # 'domain': [('id', 'in', rec.assignment_ids.ids)],
                'context':{'default_teacher_id': self.id}
            }
