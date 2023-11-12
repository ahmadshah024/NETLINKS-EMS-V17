# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsExamTimetable(models.Model):
    _name = 'ems.exam.timetable'
    _description = 'ems exam timetable'

    name = fields.Char(states={'done': [('readonly', True)]}, required=True)
    academic_year = fields.Date(states={'done': [('readonly', True)]})
    exam_type = fields.Selection([('Mid_Term','Mid Term'),('Final','Final')])
    state = fields.Selection([('draft','Draft'),('done', 'Done'), ('cancel', 'Caneled')], default='draft')
    company_id = fields.Many2one('res.company' , default=lambda self: self.env.company.id)

    exam_timetable_line_ids = fields.One2many('ems.exam.timetable.line','exam_timetable_id', states={'done': [('readonly', True)]})



    def action_done(self):
        for rec in self:
            rec.state = 'done'


    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'



class EmsExamTimetableLine(models.Model):
    _name = 'ems.exam.timetable.line'
    _description = 'ems exam timetable line description'

    exam_date = fields.Date()
    week_day = fields.Char(compute='_compute_week_day')
    # week_day = fields.Char()
    subject_id = fields.Many2one('ems.subject')
    start_time = fields.Float()
    end_time = fields.Float()
    teacher_id = fields.Many2one('hr.employee', domain=[('is_teacher', '=', True)])
    class_id = fields.Many2one('ems.class.room')

    exam_timetable_id = fields.Many2one('ems.exam.timetable')



    @api.depends('exam_date')
    def _compute_week_day(self):
        for record in self:
            if record.exam_date:
                exam_datetime = fields.Date.from_string(record.exam_date)
                day_of_week = exam_datetime.weekday()
                weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                record.week_day = weekday_names[day_of_week]
            else:
                record.week_day = False

