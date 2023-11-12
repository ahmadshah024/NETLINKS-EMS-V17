# -*- coding: utf-8 -*-

from odoo import models, fields


class ClassRoom(models.Model):
    _inherit = 'ems.subject'


    book_id = fields.Many2one('ems.book')
        
