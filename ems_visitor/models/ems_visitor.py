# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsVisitor(models.Model):
    _name = 'ems.visitor'
    _description = 'ems.visitor'

    name = fields.Char(required=True) 
    reason = fields.Text(required=True)
    through_a_friend = fields.Boolean()
    on_TV = fields.Boolean()
    on_the_radio = fields.Boolean()
    from_an_ad = fields.Boolean()
    local_community = fields.Boolean()
    social_media = fields.Selection([
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('youtube', 'Youtube'),
    ])
    # date_time = fields.Date(default=fields.Date.today())
    date_time = fields.Datetime(default=lambda self: fields.Datetime.now())



     
