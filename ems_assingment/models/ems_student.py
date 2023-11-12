# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ClassRoom(models.Model):
    _inherit = 'ems.student'


    assignment_count = fields.Integer(compute='_compute_assignment_count')

    def action_submit(self):
        return {
        'type': 'ir.actions.act_window',
        'name': 'Assignment',
        'res_model': 'submit.assignment.wizard',
        'view_type': 'form',
        'view_mode': 'form',
        'context': {'default_class_id': self.class_id.id},
        'target': 'new',
    }
    

    @api.depends('class_id')
    def _compute_assignment_count(self):
        for student in self:
            assignments = self.env['ems.assignment'].search([
                ('class_id', '=', student.class_id.id),
                ('state', '=', 'active')
            ])
            student.assignment_count = len(assignments)
     

    def action_open_assignment(self):
        for rec in self:
            return {
                'name': 'Active Assignments',
                'type': 'ir.actions.act_window',
                'res_model': 'ems.assignment',
                'view_mode': 'tree,form',
                'domain': [('class_id', '=', rec.class_id.id)],
            }
