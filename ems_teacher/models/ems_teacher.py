# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import html_escape

class EmsTeacher(models.Model):
    _inherit = "hr.employee"
    _description = 'ems teacher inherited  description'


    is_teacher = fields.Boolean("Is Teacher")
    work_phone = fields.Char(default="")
    salary = fields.Integer("Salary")
    category_ids = fields.Many2many(placeholder='subjects')
    reference = fields.Char("Reference No", required=True,copy=False,readonly=True,default='New' )
    transport_id = fields.Many2one('ems.transport')
    class_id = fields.Many2one('ems.class.room')
    
    teacher_line_ids = fields.One2many('ems.teacher.availability', 'teacher_id')
    @api.model
    def create(self, vals):   
        vals['reference'] = self.env['ir.sequence'].next_by_code('ems.teacher.sequence')
        return super(EmsTeacher, self).create(vals)
    




# class EmsTeacherLine(models.Model):
#     _name = 'ems.teacher.line'
#     _discription = 'ems teacher line description'


class EmsTeacherAvailability(models.Model):
    _name = 'ems.teacher.availability'
    _description = 'Teacher Availability'

    
    class_id = fields.Many2one('ems.class.room')
    period_count = fields.Integer('Count')
    teacher_id = fields.Many2one('hr.employee')



