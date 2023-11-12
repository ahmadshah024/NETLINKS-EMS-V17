# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class ChangeSchoolWizard(models.TransientModel):
    _name = 'change.school.wizard'
    _description = 'Accept Reason'

    reason = fields.Text(required=True)
    new_school_name = fields.Char()
    files = fields.Binary()
    student_id = fields.Many2one('ems.student')
    date = fields.Date(default=fields.Date.context_today)
    docs = fields.Binary('documents')
    def action_change(self):
        for rec in self:
            rec.student_id.write({
                'new_reason': rec.reason,
                'new_school': rec.new_school_name,
                'documents': rec.docs,
                'new_school_date': rec.date,
            })
            rec.student_id.state = 'change'