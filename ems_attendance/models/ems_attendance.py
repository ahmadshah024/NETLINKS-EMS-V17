# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EmsAttendance(models.Model):
    _name = 'ems.attendance'
    _description = 'ems attendance description'


    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='State', default='draft', )


    name = fields.Char(readonly=True, default='New')

    date = fields.Date(states={'done': [('readonly', True)]}, default=lambda self: fields.Date.today())
    class_id = fields.Many2one('ems.class.room', states={'done': [('readonly', True)]})
    attendance_line_ids = fields.One2many('ems.attendance.line','attendance_id', string='Students in Class', compute='_compute_student_ids',states={'done': [('readonly', True)]}, store=True, readonly=False)
    company_id = fields.Many2one('res.company' , default=lambda self: self.env.company.id)


    @api.model
    def create(self, vals):
        vals['name'] = f"ATT/{vals['date']}/{self.env['ir.sequence'].next_by_code('ems.attendance.sequences.sheet')}"
        return super(EmsAttendance, self).create(vals)
    
    def action_mark_done(self):
        for record in self:
            record.state = 'done'

    @api.depends('class_id')
    def _compute_student_ids(self):
        for record in self:
            if record.class_id:
                students = record.class_id.student_ids
                record.attendance_line_ids = [(0, 0, {'student_id': student.id}) for student in students]
            else:
                record.attendance_line_ids = False

    
    def action_mark_cancel(self):
        for record in self:
            record.state = 'cancel'

    def action_mark_draft(self):
        for record in self:
            record.state = 'draft'   


class EmsAttendanceLine(models.Model):
    _name = 'ems.attendance.line'
    _description = 'ems attendance line description'


    student_id = fields.Many2one('ems.student')
    is_present = fields.Boolean(default=True)
    is_absent = fields.Boolean(default=False)
    is_leave = fields.Boolean(default=False)
    attendance_id = fields.Many2one('ems.attendance')
    

    @api.onchange('is_present')
    def _onchange_is_present(self):
        if self.is_present:
            self.is_absent = self.is_leave = False

            

    @api.onchange('is_absent')
    def _onchange_is_absent(self):
        if self.is_absent:
            self.is_present = self.is_leave = False

    @api.onchange('is_leave')
    def _onchange_is_leave(self):
        if self.is_leave:
            self.is_absent = self.is_present = False
      