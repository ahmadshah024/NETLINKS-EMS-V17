# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsTeacher(models.Model):
    _inherit = 'hr.employee'


    subject_ids = fields.Many2many('ems.subject')




class EmsTeacher(models.Model):
    _inherit = 'ems.teacher.availability'

    subject_id = fields.Many2one('ems.subject')
    


