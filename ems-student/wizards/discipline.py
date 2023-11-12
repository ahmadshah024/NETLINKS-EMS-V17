

from odoo import models, fields, api

class Discipline(models.TransientModel):
    _name = 'discipline.wizard'
    _description = 'Report Reason'

    
    reason = fields.Text(required=True)
    student_id = fields.Many2one('ems.student')

    def action_report(self):
        for rec in self:
            rec.student_id.write({
                'discipline_reason': rec.reason,
            })
            
