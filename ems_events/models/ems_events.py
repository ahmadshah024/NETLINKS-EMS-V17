# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsEvent(models.Model):
    _name = 'ems.event'
    _description = 'ems event'

    name = fields.Char(required=True, states={'done': [('readonly', True)]})
    reason = fields.Text(states={'done': [('readonly', True)]})
    date =fields.Date(states={'done': [('readonly', True)]})
    teacher_id = fields.Many2one('hr.employee', states={'done': [('readonly', True)]}, domain=[('is_teacher','=', True)])
    event_category = fields.Selection([
        ('academic','Academic'),
        ('sports','Sports'),
        ('cultural','Cultural'),
        ('community','Community'),
        ('graduation','Graduation'),
        ('parent_teacher','Parent-Teacher'),
        ('art_and_Craft_exhibitions','Art and Craft Exhibitions'),
        ('science_fairs','Science Fairs'),
        ('special_celebrations','Special Celebrations'),
        ('workshops_and_training','Workshops and Training'),
    ], states={'done': [('readonly', True)]})
    state = fields.Selection([('draft','Draft'),('done', 'Done'), ('cancel', 'Caneled')], default='draft')
    event_line_ids = fields.One2many('ems.event.line', 'event_id')



    def action_done(self):
        for rec in self:
            rec.state = 'done'


    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


class EmsEventLine(models.Model):
    _name = 'ems.event.line'
    _description = 'ems event line'


    student_id = fields.Many2one('ems.student')
    father_name = fields.Char(related='student_id.father_name')
    class_id = fields.Many2one(related='student_id.class_id')
    phone = fields.Char(related='student_id.phone')
    
    
    event_id = fields.Many2one('ems.event')
