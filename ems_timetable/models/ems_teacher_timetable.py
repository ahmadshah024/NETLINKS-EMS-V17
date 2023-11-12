# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsTeacherTimetable(models.Model):
    _name = 'ems.teacher.timetable'
    _description = 'ems teacher timetable'


    name = fields.Char()
    teacher_id = fields.Many2one('hr.employee', domain=[('is_teacher', '=', True)])
    period = fields.Date()
    line_ids = fields.One2many('ems.teacher.timetable.line', 'teacher_timetable_id')


class EmsTeacherTimetableLine(models.Model):
    _name = 'ems.teacher.timetable.line'
    _description = 'ems teacher timetable line'


    days = fields.Selection([
        ('saturday','Saturday'),
        ('sunday','Sunday'),
        ('monday','Monday'),
        ('tuesday','Tuesday'),
        ('wednesday','Wednesday'),
        ('thursday','Thursday'),
    ])

    start_time = fields.Float()
    end_time = fields.Float()
    duration = fields.Float(compute="_compute_duration_time")
    subject_id = fields.Many2one('ems.subject')
    class_id = fields.Many2one('ems.class.room')
    teacher_timetable_id = fields.Many2one('ems.teacher.timetable')




    @api.depends('start_time', 'end_time')
    def _compute_duration_time(self):
        for rec in self:
            start_time_minutes = int(rec.start_time) * 60 + (rec.start_time - int(rec.start_time)) * 100
            end_time_minutes = int(rec.end_time) * 60 + (rec.end_time - int(rec.end_time)) * 100

            rec.duration = end_time_minutes - start_time_minutes

