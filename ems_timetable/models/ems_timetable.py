# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmsTimetable(models.Model):
    _name = 'ems.timetable'
    _description = 'ems timetable'

    name = fields.Char(states={'done': [('readonly', True)]}, required=True)
    academic_year = fields.Date(states={'done': [('readonly', True)]})
    class_ids = fields.Many2many('ems.class.room', states={'done': [('readonly', True)]}, required=True)
    class_id = fields.Many2one('ems.class.room')
    day_ids = fields.Many2many('ems.timetable.day')
    period_count = fields.Integer('Period Per Week')
    subject_ids = fields.Many2many('ems.subject')
    teacher_ids = fields.Many2many('hr.employee', domain=[('is_teacher', '=', True)])
    # class_ids = fields.Many2many('ems.class.room', states={'done': [('readonly', True)]}, required=True)
    state = fields.Selection([('draft','Draft'),('done', 'Done'), ('cancel', 'Caneled')], default='draft')
    company_id = fields.Many2one('res.company' , default=lambda self: self.env.company.id)
    timetable_line_ids = fields.One2many('ems.timetable.line','timetable_id', states={'done': [('readonly', True)]})



    def action_done(self):
        for rec in self:
            rec.state = 'done'


    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


    MAX_PERIODS_PER_WEEK = 36  # Maximum periods a teacher can teach in a week

    def generate_timetable(self):
        # Clear existing timetable lines
        self.env['ems.timetable.line'].search([]).unlink()

        # Get teachers and classes
        teachers = self.env['hr.employee'].search([('is_teacher','=', True)])
        classes = self.env['ems.class.room'].search([])

        # Define a list of days
        days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday']


        # Get the teaching periods from ems.timetable.period.line
        teaching_periods = self.env['ems.timetable.period.line'].search([])

        # Initialize a dictionary to track the number of periods assigned to each teacher
        teacher_periods_count = {}

        # Loop through days, teaching periods, teachers, and classes to create timetable lines
        for day in days:
            for period in teaching_periods:
                for teacher in teachers:
                    for class_obj in classes:
                        # Check if the teacher is available at this time
                        if self.is_teacher_available(teacher, day, period):
                            # Check if the classroom is available at this time
                            if self.is_classroom_available(class_obj, day, period):
                                # Select a subject for this slot (ensure not back-to-back)
                                subject = self.select_subject(teacher, class_obj, day, period)

                                if subject:
                                    # Update the teacher's period count
                                    teacher_periods_count[teacher] = teacher_periods_count.get(teacher, 0) + 1

                                    if teacher_periods_count[teacher] <= self.MAX_PERIODS_PER_WEEK:
                                        # Create a timetable line
                                        timetable_line_ids = self.env['ems.timetable.line'].create({
                                            'teacher_id': teacher.id,
                                            'class_id': class_obj.id,
                                            'subject_id': subject.id,
                                            'day': day,
                                            'start_time': period.start_time,
                                            'end_time': period.end_time,
                                        })

    def is_teacher_available(self, teacher, day, period):
    # Implement logic to check teacher availability
    # This might involve querying the teacher's schedule or availability model
    # Return True if the teacher is available, otherwise return False
    # You should check that the teacher is not scheduled for another class at this time
    # If the teacher is available, return True; otherwise, return False
    # For example, check if the teacher has no existing class at this time
        is_teacher_scheduled = self.env['ems.timetable.line'].search([
            ('teacher_id', '=', teacher.id),
            ('day', '=', day),
            # ('start_time', '<', period.end_time),
            # ('end_time', '>', period.start_time),
        ])
        return not is_teacher_scheduled

    def is_classroom_available(self, class_obj, day, period):
        # Implement logic to check classroom availability
        # This might involve querying the classroom's schedule or availability model
        # Return True if the classroom is available, otherwise return False
        # You should check that the classroom is not scheduled for another class at this time
        # If the classroom is available, return True; otherwise, return False
        # For example, check if the classroom has no existing class at this time
        is_classroom_scheduled = self.env['ems.timetable.line'].search([
            ('class_id', '=', class_obj.id),
            ('day', '=', day),
            # ('start_time', '<', period.end_time),
            # ('end_time', '>', period.start_time),
        ])
        return not is_classroom_scheduled

    def select_subject(self, teacher, class_obj, day, period):
    # Your logic for selecting a subject that is not back-to-back
    # Implement this logic based on your specific constraints
    # Return the selected subject or None if no subject is available

    # For example, you might query available subjects for the given teacher and class
        available_subjects = self.get_available_subjects(teacher, class_obj, day, period)

        # Implement your selection logic here (e.g., random selection, prioritizing subjects, etc.)
        if available_subjects:
            selected_subject = available_subjects[0]  # Example: Select the first available subject
            return selected_subject

        return None  # Return None if no subject is available

    def get_available_subjects(self, teacher, class_obj, day, period):
        # Query available subjects based on teacher, class, day, and period
        # Implement your specific query logic here to retrieve available subjects
        # You may need to consider teacher and class preferences, curriculum, and other constraints
        available_subjects = self.env['ems.subject'].search([
            ('teacher_ids', 'in', [teacher.id]),  # Example: Subjects taught by the teacher
            ('class_line_ids', 'in', [class_obj.id]),  # Example: Subjects assigned to the class
        ])
        return available_subjects
    
    
class EmsTimetableLine(models.Model):
    _name = 'ems.timetable.line'
    _description = 'ems timetable line description'

    day = fields.Selection([
        ('saturday','Saturday'),
        ('sunday','Sunday'),
        ('monday','Monday'),
        ('tuesday','Tuesday'),
        ('wednesday','Wednesday'),
        ('thursday','Thursday'),
    ])
    teacher_id = fields.Many2one('hr.employee', domain=[('is_teacher', '=', True)])
    class_id = fields.Many2one('ems.class.room')
    subject_id = fields.Many2one('ems.subject')


    # subject_id1 = fields.Many2one('ems.subject')
    # subject_id2 = fields.Many2one('ems.subject')
    # subject_id3 = fields.Many2one('ems.subject')
    # subject_id4 = fields.Many2one('ems.subject')
    # subject_id5 = fields.Many2one('ems.subject')
    # subject_id6 = fields.Many2one('ems.subject')
    # subject_id7 = fields.Many2one('ems.subject')
    # subject_id8 = fields.Many2one('ems.subject')
    # subject_id9 = fields.Many2one('ems.subject')
    
    
    timetable_id = fields.Many2one('ems.timetable')

    subject_ids = fields.Many2many('ems.subject', string='Subjects', compute='_compute_subjects')
    timetable_id = fields.Many2one('ems.timetable')

    # @api.depends('timetable_id.subject_count')
    # def _compute_subjects(self):
    #     for record in self:
             


class EmsTimetablePeriod(models.Model):
    _name = 'ems.timetable.period'
    _description = 'ems timetable period description'


    name = fields.Char()

    period_line_ids = fields.One2many('ems.timetable.period.line', 'period_id')


class EmsTimetablePeriodLine(models.Model):
    _name = 'ems.timetable.period.line'
    _description = 'ems timetable period line description'


    number = fields.Integer('No')
    start_time = fields.Float()
    end_time = fields.Float()
    length = fields.Float(compute="_compute_length")
    period_id = fields.Many2one('ems.timetable.period')





    @api.depends('start_time', 'end_time')
    def _compute_length(self):
        for rec in self:
            start_time_minutes = int(rec.start_time) * 60 + (rec.start_time - int(rec.start_time)) * 100
            end_time_minutes = int(rec.end_time) * 60 + (rec.end_time - int(rec.end_time)) * 100

            rec.length = end_time_minutes - start_time_minutes


class EmsTimetableDay(models.Model):
    _name = 'ems.timetable.day'
    _description = 'ems timetable day description'


    name = fields.Char()
    
    day_line_ids = fields.One2many('ems.timetable.day.line', 'day_id')


class EmsTimetableDayLine(models.Model):
    _name = 'ems.timetable.day.line'
    _description = 'ems timetable day line description'


    name = fields.Char()

    day_id = fields.Many2one('ems.timetable.day')    
