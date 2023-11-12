# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError



class EmsLibrary(models.Model):
    _name = 'ems.library'
    _description = 'ems_library'

    name = fields.Char(readonly=True, default="New", states={'done': [('readonly', True)]})
    date = fields.Date(string='Date', default=lambda self: fields.Date.today(), states={'done': [('readonly', True)]})
    days = fields.Integer(string='Days', states={'done': [('readonly', True)]},required=True)
    return_date = fields.Date(string='Return Date', compute='_compute_return_date', store=True, states={'done': [('readonly', True)]})
    student_id = fields.Many2one('ems.student', states={'done': [('readonly', True)]}, required=True)
    library_line_ids = fields.One2many('ems.library.line', 'library_id', states={'done': [('readonly', True)]})
    is_returned = fields.Boolean(default=False, states={'done': [('readonly', True)]})
    state = fields.Selection([
    ('draft', 'Draft'),
    ('waiting', 'Waiting'),
    ('return', 'Returned'),
    ('done', 'Done'),
    ('cancel', 'Cancel'),
    ], string='State', default='draft', states={'done': [('readonly', True)]})


    def action_mark_done(self):
        for record in self:
            if not record.is_returned:
                raise ValidationError('The book has not been returned yet')
            for library_line in record.library_line_ids:
                book = library_line.book_id
                if book.copy_amount >= book.available:
                    book.available += 1
                else:
                   raise ValidationError(f'Book "{book.name}" is returned') 
                book.state = 'free'
            record.state = 'done'
   

    def action_mark_cancel(self):
        for record in self:
            record.state = 'cancel'

    def action_mark_return(self):
        for record in self:
            record.is_returned = True
            record.state = 'return'
 
    def action_mark_waiting(self):
        for record in self:
            books_to_check = set()
            for library_line in record.library_line_ids:
                book = library_line.book_id
                if book.copy_amount <= 0:
                    raise ValidationError(f'No more copies available for book "{book.name}"')
                if book.available == 0 and library_line.book_id.state == 'free':
                    book.available = book.copy_amount
                if book.available <= 0:
                    raise ValidationError(f'Book "{book.name}" is not available')
                books_to_check.add(book.id)
                book.available -= 1
            if len(books_to_check) < len(record.library_line_ids):
                raise ValidationError('Duplicate books selected in the request')
            record.library_line_ids.book_id.write({'state': 'assigned'})
            record.state = 'waiting'

 

    @api.depends('date', 'days')
    def _compute_return_date(self):
        for request in self:
            if request.date and request.days:
                return_date = request.date + timedelta(days=request.days)
                request.return_date = return_date
            else:
                request.return_date = False




    @api.model
    def create(self, vals):   
        vals['name'] = self.env['ir.sequence'].next_by_code('ems.library.sequence')
        return super(EmsLibrary, self).create(vals)
    
    



class EmsLibraryLine(models.Model):
    _name = 'ems.library.line'
    _description = 'ems_library'

    library_id = fields.Many2one('ems.library')
    
    book_id = fields.Many2one('ems.library.books') 
    author = fields.Char(related='book_id.author')
    language = fields.Char(related='book_id.language')
    subjects = fields.Char( related='book_id.subjects')
 


class EmsBook(models.Model):
    _name = 'ems.library.books'
    _description = 'ems.library.book'

    name = fields.Char()
    author = fields.Char()
    pages = fields.Char()
    subjects = fields.Char()
    title = fields.Char(string='Title', required=True)
    language = fields.Char(string='Language')
    cover_image = fields.Binary(string='Cover Image')
    publication_date = fields.Date(string='Publication Date')
    description = fields.Text(string='Description')
    copy_amount = fields.Integer(string='Copy Amount')
    available = fields.Integer(string='Available Amount', readonly=True)
    state = fields.Selection([
        ('free', 'Free'),
        ('assigned', 'Assigned'),
    ], string='State', default='free')


    library_line_ids = fields.One2many('ems.library.line','book_id')
 
    assigned_students_count = fields.Integer(compute='_compute_assigned_students_count', string='Assigned Students Count')
    assigned_students = fields.Many2many('ems.student', compute='_compute_assigned_students', string='Assigned Students')

    def _compute_assigned_students_count(self):
        for book in self:
            book.assigned_students_count = len(book.assigned_students)

    def _compute_assigned_students(self):
        for book in self:
            book.assigned_students = book.library_line_ids.mapped('library_id.student_id')


    def action_open_library(self):
        for rec in self:
            # book_ids = rec.curriculum_line_ids.mapped('book_id')
            return {
                'name': 'Requests',
                'type': 'ir.actions.act_window',
                'res_model': 'ems.student',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', rec.library_line_ids.ids)],
            }
        



    
  





    