# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date
from string import digits
from random import choice



class EmsStudent(models.Model):
    _name = 'ems.student'
    _description = 'ems student description'

    reference = fields.Char("Reference No", required=True,copy=False,readonly=True,default='New' )
    image = fields.Binary(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    name = fields.Char(states={'done': [('readonly', True)],'graduate': [('readonly', True)], 'change': [('readonly', True)]}, required=True)

    father_name = fields.Char(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    grand_father_name = fields.Char(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    address = fields.Char(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    phone = fields.Char(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    email = fields.Char(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    nic = fields.Char('Tazkira No', required=True, states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    dob = fields.Date(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    age = fields.Char(compute='_compute_age', store=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    student_document = fields.Binary(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    parent_id = fields.Many2one('ems.parent', states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    school = fields.Many2one('res.company', states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    class_id = fields.Many2one('ems.class.room', states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    country_id = fields.Many2one('res.country', states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]}  ,default=lambda self: self.env['res.country'].search([('name', '=', 'Afghanistan'), ('code', '=', 'AF')]))
    province_id = fields.Many2one('res.country.state', states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]} ,domain="[('country_id', '=', country_id)]", string="Province/State")
    district_id = fields.Many2one('ems.district', domain="[('province_id', '=', province_id)]", states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    academic_year = fields.Date(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    date = fields.Date(default=lambda self: fields.Date.today(),states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    parent_name = fields.Char(related='parent_id.name', states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    previous_school_name = fields.Char('School Name',states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    previous_school_registration_no = fields.Char('Registration No', states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    previous_school_addmission_date = fields.Date('Addmission Date', states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    previous_school_exit_date = fields.Date('Exit Date', states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    previous_school_exit_reason = fields.Text(states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    previous_school_document_file = fields.Binary('Documents')
    remarks = fields.Html(states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    award_ids = fields.One2many('ems.student.award','student_id', states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    certificate_ids = fields.One2many('ems.student.certificate','student_id', states={'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    state = fields.Selection([('draft','Draft'),('done', 'Done'), ('cancel', 'Caneled'), ('graduate', 'Graduated'), ('change','Changed')], default='draft')
    is_new = fields.Boolean('Is New', states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    is_changed = fields.Boolean('Is Change', states={'done': [('readonly', True)], 'graduate': [('readonly', True)], 'change': [('readonly', True)]})
    company_id = fields.Many2one('res.company')
    new_school = fields.Char(readonly=True)
    new_reason = fields.Char(readonly=True)
    new_school_date = fields.Date(readonly=True)
    documents = fields.Binary(readonly=True)
    avatar_1920 = fields.Image("Avatar")
    event_id = fields.Many2one('ems.event')
    transport_id = fields.Many2one('ems.transport')
    barcode = fields.Char(string="Badge ID", help="ID used for employee identification.", copy=False)
    pin = fields.Char(string="PIN", groups="hr.group_hr_user", copy=False,
        help="PIN used to Check In/Out in the Kiosk Mode of the Attendance application (if enabled in Configuration) and to change the cashier in the Point of Sale application.")
    
    discipline_reason = fields.Text(readonly=True)
    # is_persent = fields.Boolean(default=False)
    # is_absent = fields.Boolean(default=False)
    # is_leave = fields.Boolean(default=False)
    
    _sql_constraints = [
        ('barcode_uniq', 'unique (barcode)', "The Badge ID must be unique, this one is already assigned to another employee."),
        ('user_uniq', 'unique (user_id, company_id)', "A user cannot be linked to multiple employees in the same company.")
    ]
    def generate_random_barcode(self):
        for employee in self:
            employee.barcode = '041'+"".join(choice(digits) for i in range(9))


    def action_change_new_flase(self):
        for rec in self:
            if rec.is_new or rec.is_changed:
                rec.is_new = False
                rec.is_changed = False
                


    def action_done(self):
        for rec in self:
            if rec.is_new:
                raise ValidationError('This Student is new, please the check the documentes first')
            elif rec.is_changed:
                raise ValidationError('This Student is changed, please the check the documentes first')
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_graduate(self):
        for rec in self:
            rec.state = 'graduate'
        
    def action_change(self):
        return {
        'type': 'ir.actions.act_window',
        'name': 'New School',
        'res_model': 'change.school.wizard',
        'view_type': 'form',
        'view_mode': 'form',
        'target': 'new',
        'context':{'default_student_id': self.id}
    }
    
    def action_report(self):
        return {
        'type': 'ir.actions.act_window',
        'name': 'Student Report Discipline',
        'res_model': 'discipline.wizard',
        'view_type': 'form',
        'view_mode': 'form',
        'target': 'new',
        'context':{'default_student_id': self.id}
    }
    
    _sql_constraints = [
        ('name_unique', 'unique(nic)',
         "Please Check the NIC Number, already exists!"),
    ]
    

    @api.model
    def create(self, vals):   
        vals['reference'] = self.env['ir.sequence'].next_by_code('ems.student.sequence')
        return super(EmsStudent, self).create(vals)
    

    @api.depends('dob')
    def _compute_age(self):
        for patient in self:
            patient.age = False
            if patient.dob:
                if patient.dob > datetime.today().date():
                    raise ValidationError("Invalid date of birth, Please choose a date equal or older than today.")
                today = date.today()
                dob = patient.dob
                patient.age = today.year - dob.year - \
                    ((today.month, today.day) < (dob.month, dob.day))



class EmsStudentAward(models.Model):
    _name = 'ems.student.award'
    _description = 'ems student award description'


    name = fields.Char()
    description = fields.Text()

    student_id = fields.Many2one('ems.student')

class EmsStudentCertificate(models.Model):
    _name = 'ems.student.certificate'
    _description = 'ems student certificate description'


    certificate = fields.Binary()
    description = fields.Text()

    student_id = fields.Many2one('ems.student')

class EmsClassRoom(models.Model):
    _name = 'ems.class.room'
    _description = 'ems class room description'


    name = fields.Char('Name', required=True)
    block = fields.Char('Block')
    room_number = fields.Char('Room Number')
    class_line_ids = fields.One2many('ems.class.room.line', 'class_id')

    student_ids = fields.One2many('ems.student', 'class_id')
    student_count = fields.Integer(compute="_compute_student_count")

    def _compute_student_count(self):
        for record in self:
            student_count = len(record.student_ids)
            record.student_count = student_count

    def action_open_students(self):
        for rec in self:
            return {
                'name': 'Students',
                'type': 'ir.actions.act_window',
                'res_model': 'ems.student',
                'view_mode': 'tree,form',
                'domain': [('class_id', '=', rec.id)],
            }
        
    

class EmsClassRoomline(models.Model):
    _name = 'ems.class.room.line'
    _description = 'ems class room line description'


    # subject_id = fields.Many2one('ems.subject')
    # book_id = fields.Many2one('ems.book')
    class_id = fields.Many2one('ems.class.room')
    # max_mark = fields.Integer(related='subject_id.maximum_mark')
    # min_mark = fields.Integer(related='subject_id.minimum_mark')
    # teacher_id = fields.Char()
