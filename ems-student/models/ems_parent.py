# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsParent(models.Model):
    _inherit = 'ems.parent'

    student_ids = fields.One2many('ems.student','parent_id')
