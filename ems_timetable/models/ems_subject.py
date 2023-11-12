# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsSubject(models.Model):
    _name = 'ems.subject'
    _description = 'ems subject description'

    name = fields.Char(required=True, states={'done': [('readonly', True)]})
    maximum_mark = fields.Integer(states={'done': [('readonly', True)]})
    code = fields.Char(readonly=True, default='New')
    minimum_mark = fields.Integer(states={'done': [('readonly', True)]})
    is_practical = fields.Boolean(states={'done': [('readonly', True)]})
    state = fields.Selection([('draft','Draft'),('done', 'Done'), ('cancel', 'Caneled')], default='draft')
    teacher_id = fields.Many2one('hr.employee', domain=[('is_teacher', '=', True)])
    # book_id = fields.Many2one('ems.book')
    # class_line_ids = fields.One2many('ems.subject.line','subject_id', states={'done': [('readonly', True)]})
    # teacher_line_ids = fields.One2many('ems.subject.line.teacher','subject_id', states={'done': [('readonly', True)]})


    def action_done(self):
        for rec in self:
            rec.state = 'done'


    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
    @api.model
    def create(self, vals):   
        vals['code'] = self.env['ir.sequence'].next_by_code('ems.subject.sequence')
        return super(EmsSubject, self).create(vals)
    

# class EmsSubjectLine(models.Model):
#     _name = 'ems.subject.line'
#     _description = 'ems subject line description'


#     class_id = fields.Many2one('ems.class.room')
#     block = fields.Char(related='class_id.block')
#     room = fields.Char(related='class_id.room_number')
#     subject_id = fields.Many2one('ems.subject')


# class EmsSubjectLineTeacher(models.Model):
#     _name = 'ems.subject.line.teacher'
#     _description = 'ems subject line teacher description'

#     phone = fields.Char(related='teacher_id.work_phone')
#     email = fields.Char(related='teacher_id.work_email')
#     department = fields.Many2one(related='teacher_id.department_id')
#     job = fields.Char(related='teacher_id.job_title')
#     subject_id = fields.Many2one('ems.subject')


