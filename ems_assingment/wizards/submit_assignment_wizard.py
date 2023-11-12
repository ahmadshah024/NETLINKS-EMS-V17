# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class ChangeSchoolWizard(models.TransientModel):
    _name = 'submit.assignment.wizard'
    _description = ' submite assignment description'


    class_id = fields.Many2one('ems.class.room')
    
    assignment_id = fields.Many2one('ems.assignment', domain="[('class_id', '=' , class_id),('state', '=', 'active')]", required=True)

    file = fields.Binary(required=True)
    date = fields.Date(default=fields.Date.context_today)
    

    def action_submit(self):
            for rec in self:
                if rec.assignment_id.state != 'done':
                    existing_submission = rec.env['ems.assignment.line'].search([
                        ('assignment_id', '=', rec.assignment_id.id),
                        ('student_id', '=', rec.env.context.get('active_id'))
                    ])

                    if not existing_submission:
                        rec.env['ems.assignment.line'].create({
                            'submitted_date': rec.date,
                            'documents': rec.file,
                            'assignment_id': rec.assignment_id.id,
                            'student_id': rec.env.context.get('active_id')
                        })
                    else:
                        raise ValidationError('You have already submitted this assignment.')
                else:
                    raise ValidationError('The homework cannot be submitted because the due date is overdue.')



    # def action_submit(self):
    #     for rec in self:
    #         if rec.assignment_id.state != 'done':
    #             existing_submission = rec.env['ems.assignment.line'].search([
    #                 ('assignment_id', '=', rec.assignment_id.id),
    #                 ('student_id', '=', rec.env.context.get('active_id'))
    #             ])

    #             if not existing_submission:
    #                 rec.env['ems.assignment.line'].create({
    #                     'submitted_date': rec.date,
    #                     'documents': rec.file,
    #                     'assignment_id': rec.assignment_id.id,
    #                     'student_id': rec.env.context.get('active_id')
    #                 })
    #             else:
    #                 raise ValidationError('You have already submitted this assignment.')
    #         else:
    #             raise ValidationError('The homework cannot be submitted because the due date is overdue.')

    # def action_submit(self):
    #     for rec in self:
    #         if rec.assignment_id.state != 'done':
    #             rec.env['ems.assignment.line'].create({
    #                 'submitted_date': rec.date,
    #                 'documents': rec.file,
    #                 'assignment_id': rec.assignment_id.id,
    #                 'student_id': rec.env.context.get('active_id')
    #             })
    #         else:
    #             raise ValidationError('the home work can not be submitted because the due date is overed')

