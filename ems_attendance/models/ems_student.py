# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class EmsStudent(models.Model):
    _inherit = 'ems.student'

    attendance_id = fields.Many2one('ems.attendance')
    
    present_count = fields.Integer(compute='_compute_present_count', string='Present Days')
    absent_count = fields.Integer(compute='_compute_absent_count', string='Absent Days')
    leave_count = fields.Integer(compute='_compute_leave_count', string='Leave Days')


    @api.depends('attendance_id')
    def _compute_present_count(self):
        for rec in self:
            rec.present_count = rec.env['ems.attendance.line'].search_count([
                ('student_id', '=', rec.id),
                ('is_present', '=', True),
            ])

    @api.depends('attendance_id')
    def _compute_absent_count(self):
        for rec in self:
            rec.absent_count = rec.env['ems.attendance.line'].search_count([
                ('student_id', '=', rec.id),
                ('is_absent', '=', True),
            ])
    @api.depends('attendance_id')
    def _compute_leave_count(self):
        for rec in self:
            rec.leave_count = rec.env['ems.attendance.line'].search_count([
                ('student_id', '=', rec.id),
                ('is_leave', '=', True),
            ])


    def action_open_attendane(self):
        for rec in self:
            return {
                'name': 'Attendane',
                'type': 'ir.actions.act_window',
                'res_model': 'ems.attendance',
                'view_mode': 'tree,form',
                'domain': [('class_id', '=', rec.class_id.id)],
                'context': {
                    'default_student_id': rec.id,
                },
            }