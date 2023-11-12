# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EmsExamination(models.Model):
    _name = 'ems.examination'
    _description = 'ems_examination'


    reference = fields.Char(readonly=True, default="New", states={'finished': [('readonly', True)]})
    name = fields.Char(required=True, states={'finished': [('readonly', True)]})
    start_date = fields.Date(required=True, states={'finished': [('readonly', True)]})
    end_date = fields.Date(required=True, states={'finished': [('readonly', True)]})
    academic_year = fields.Char(states={'finished': [('readonly', True)]})
    exam_type = fields.Selection([
        ('mid-term', 'Mid-term'),
        ('final', 'Final'),
        ('other', 'Other'),
    ], required=True, states={'finished': [('readonly', True)]})

    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('finished', 'Finished'),
        ('cancel', 'Cancel'),
    ], string='State', default='draft', states={'finished': [('readonly', True)]})
    examination_line_ids = fields.One2many('ems.examination.line', 'examination_id', states={'finished': [('readonly', True)]})

  
    @api.onchange('end_date')
    def _onchange_end_date(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.start_date > record.end_date:
                    raise ValidationError("End date cannot be earlier than the start date.")

    def action_mark_start(self):
        for record in self:
            record.state = 'running'

    
    def action_mark_finish(self):
        for record in self:
            record.state = 'finished'

    def action_mark_cancel(self):
        for record in self:
            record.state = 'cancel'        

    def action_mark_draft(self):
        for record in self:
            record.state = 'draft'   
    


    @api.model
    def create(self, vals):   
        vals['reference'] = self.env['ir.sequence'].next_by_code('ems.examination.sequence')
        return super(EmsExamination, self).create(vals)
    
  
   

class EmsExaminationLine(models.Model):
    _name = 'ems.examination.line'
    _description = 'ems_examination_line'

    class_id = fields.Many2one('ems.class.room')
    timetable_id = fields.Many2one('ems.exam.timetable', domain="[('exam_timetable_line_ids.class_id', '=', class_id)]")
    teacher_id = fields.Many2one('hr.employee', domain=[('is_teacher','=', True)])
    examination_id = fields.Many2one('ems.examination')
