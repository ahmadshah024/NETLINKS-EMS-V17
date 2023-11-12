# -*- coding: utf-8 -*-

from odoo import models, fields


class ClassRoom(models.Model):
    _inherit = 'ems.class.room'

    assignment_ids = fields.One2many('ems.assignment','class_id')
    assignment_count = fields.Integer(compute='_compute_assignment_count')

    def _compute_assignment_count(self):
        for rec in self:
            active_assignments = rec.assignment_ids.filtered(lambda assignment: assignment.state == 'active')
            rec.assignment_count = len(active_assignments)

    def action_open_assignment(self):
        for rec in self:
            active_assignment_ids = rec.assignment_ids.filtered(lambda assignment: assignment.state == 'active').ids
            return {
                'name': 'Active Assignments',
                'type': 'ir.actions.act_window',
                'res_model': 'ems.assignment',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', active_assignment_ids)],
            }
