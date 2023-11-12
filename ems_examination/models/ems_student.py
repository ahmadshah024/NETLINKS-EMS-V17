# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ClassRoom(models.Model):
    _inherit = 'ems.student'


    result_count = fields.Integer(compute='_compute_result_count')

    # def _compute_assignment_count(self):
    #     for rec in self:
    #         rec.assignment_count = rec.env['ems.assignment'].search_count([('class_id', '=', rec.class_id.id), ('state', '=', 'active')])


    @api.depends('class_id')
    def _compute_result_count(self):
        for student in self:
            results = self.env['ems.examination.result'].search([
                ('class_id', '=', student.class_id.id),
            ])
            student.result_count = len(results)
     

    def action_open_result(self):
        for rec in self:
            return {
                'name': 'Result',
                'type': 'ir.actions.act_window',
                'res_model': 'ems.examination.result',
                'view_mode': 'tree,form',
                'domain': [('student_id', '=', rec.id)],
                'context': {
                'default_student_id': rec.id,  # Pass the student's ID as the default value
                # 'search_default_student_id': rec.student_id.id,  # Set the search default
            },
            }
