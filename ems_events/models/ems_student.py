# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ClassRoom(models.Model):
    _inherit = 'ems.student'
 
    

    event_id = fields.Many2one('ems.event')
    event_count = fields.Integer(compute='_compute_event_count', string='Event Count')


    @api.depends('event_id')
    def _compute_event_count(self):
        for rec in self:
            rec.event_count = rec.env['ems.event.line'].search_count([
                ('student_id', '=', rec.id),
            ])
 


    def action_open_event(self):
        for rec in self:
            return {
                'name': 'Events for Student',
                'type': 'ir.actions.act_window',
                'res_model': 'ems.event',
                'view_mode': 'tree,form',
                'domain': [('event_line_ids.student_id', '=', rec.id)],
            }
    # def action_open_event(self):
    #     for rec in self:
    #         return {
    #             'name': 'Event',
    #             'type': 'ir.actions.act_window',
    #             'res_model': 'ems.event',
    #             'view_mode': 'tree,form',
    #             'domain': [('student_id', '=', rec.id)],
    #             # 'context': {
    #             #     'default_student_id': rec.id,
    #             # },
    #         }