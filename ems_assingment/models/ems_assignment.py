# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class EmsAassignment(models.Model):
    _name = 'ems.assignment'
    _description = 'ems assignment description'

    name = fields.Char(states={'active': [('readonly', True)], 'done': [('readonly', True)]})
    teacher_id = fields.Many2one('hr.employee', domain=[('is_teacher','=',True)], states={'active': [('readonly', True)], 'done': [('readonly', True)]})
    class_id = fields.Many2one('ems.class.room', states={'active': [('readonly', True)], 'done': [('readonly', True)]})
    subject_id = fields.Many2one('ems.subject', states={'active': [('readonly', True)], 'done': [('readonly', True)]})
    assign_date = fields.Date(default=fields.Date.today(), states={'active': [('readonly', True)], 'done': [('readonly', True)]})
    due_date = fields.Date(states={'active': [('readonly', True)], 'done': [('readonly', True)]})
    submission_type = fields.Selection([('handwritten','Handwritten'),('hardcopy','Hardcopy'),('submite','Submite')], states={'active': [('readonly', True)], 'done': [('readonly', True)]})
    file = fields.Binary('Attache Home', states={'active': [('readonly', True)], 'done': [('readonly', True)]})
    state = fields.Selection([('active','Active'),('done','Done'),('draft','Draft')], default='draft')
    submitted_date = fields.Date()
    documents = fields.Binary()
    assignment_line_ids = fields.One2many('ems.assignment.line', 'assignment_id')

    def action_active(self):
        for rec in self:
            rec.state = 'active'

    def action_done(self):
        for rec in self:
            if rec.due_date and rec.due_date < fields.Date.today():
                raise UserError("Cannot change state to 'done' before the due date.")
            rec.state = 'done'

    def check_due_date(self):
        today = fields.Date.today()
        overdue_assignments = self.search([('state', '=', 'active'), ('due_date', '<', today)])
        overdue_assignments.write({'state': 'done'})

class EmsAassignmentLine(models.Model):
    _name = 'ems.assignment.line'
    _description = 'ems assignment line description'

    assignment_id = fields.Many2one('ems.assignment')
    submitted_date = fields.Date()
    documents = fields.Binary()
    student_id = fields.Many2one('ems.student')




#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
