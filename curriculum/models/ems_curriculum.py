# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError



class EmsCurriculum(models.Model):
    _name = 'ems.curriculum'
    _description = 'curriculum'


    name = fields.Char(string='Curriculum Name', required=True)
    # book_name = fields.Char(string='Book Names', related='book_ids.name', store=True)
    reference = fields.Char(readonly=True, default="New")
    class_id = fields.Many2one('ems.class.room', states={'done': [('readonly', True)]})
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='State', default='draft')
    acadomic_year = fields.Date(states={'done': [('readonly', True)]})
    curriculum_line_ids = fields.One2many('ems.curriculum.line', 'curriculum_id',states={'done': [('readonly', True)]})
 
    def action_mark_done(self):
        for rec in self:
            # if rec.class_id.class_line_ids:
            #     raise  ValidationError("A curriculum already exists for this class.")
            # else:
                for line in rec.curriculum_line_ids:
                    rec.env['ems.class.room.line'].create({
                        'subject_id': line.subject_id.id,
                        'book_id': line.book_id.id,
                        'class_id': rec.class_id.id,
                    })
                rec.state = 'done'



    def action_mark_cancel(self):
        for record in self:
            record.state = 'cancel'

    def action_mark_draft(self):
        for record in self:
            record.state = 'draft'   
            record.class_id.class_line_ids.unlink()  
    

 
    @api.model
    def create(self, vals):   
        vals['reference'] = self.env['ir.sequence'].next_by_code('ems.curriculum.sequence')
        return super(EmsCurriculum, self).create(vals)
    

class EmsCurriculumLine(models.Model):
    _name = 'ems.curriculum.line'
    _description = 'ems curvericulum line'


    subject_id = fields.Many2one('ems.subject')
    book_id = fields.Many2one(related='subject_id.book_id')

    # book_id = fields.Char()
    


    curriculum_id = fields.Many2one('ems.curriculum')
    # class_id = fields.Many2one(related='curriculum_id.class_id', store=True)





class EmsBook(models.Model):
    _name = 'ems.book'
    _description = 'book'


    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='State', default='draft', states={'done': [('readonly', True)]})
    
    name = fields.Char(string='Book Name', required=True)
    publication_date = fields.Date(string='Publication Date')
    author = fields.Char()
    pages = fields.Integer()
    image = fields.Binary()

    def action_mark_done(self):
        for record in self:
            record.state = 'done'

    
    def action_mark_cancel(self):
        for record in self:
            record.state = 'cancel'

    def action_mark_draft(self):
        for record in self:
            record.state = 'draft'   
    
