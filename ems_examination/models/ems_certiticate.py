# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EmsCertificate(models.Model):
    _name = 'ems.certificate'
    _description = 'ems certificate description'


    name =  fields.Char(readonly=True, default="New")
    certificate_type = fields.Selection([('student','Student'),('teacher','Teacher')], default="student")
    certification_reason = fields.Selection([
    ('academic_achievement', 'Academic Achievement'),
    ('course_completion', 'Completion of a Course'),
    ('perfect_attendance', 'Perfect Attendance'),
    ('leadership_and_service', 'Leadership and Service'),
    ('outstanding_behavior', 'Outstanding Behavior'),
    ('community_involvement', 'Community Involvement'),
    ('special_achievements', 'Special Achievements'),
    ('character_development', 'Character Development'),
    ('graduation', 'Graduation'),
    ('perfect_conduct', 'Perfect Conduct'),
    ('honor_roll', 'Honor Roll'),
    ('sports_achievements', 'Sports Achievements'),
    ('arts_and_creativity', 'Arts and Creativity'),
    ('dedication_and_commitment', 'Dedication and Commitment')
    ], string="Certification Reason")
    student_id = fields.Many2one('ems.student')
    teacher_id = fields.Many2one('hr.employee', domain=[('is_teacher', '=', True)])
    class_id = fields.Many2one(related='student_id.class_id')
    company_id = fields.Many2one('res.company' , default=lambda self: self.env.company.id)    
    date = fields.Date(default=fields.Date.today())
    

    @api.model
    def create(self, vals):   
        vals['name'] = self.env['ir.sequence'].next_by_code('ems.certificate.sequence')
        return super(EmsCertificate, self).create(vals)
