from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EmsExaminationResult(models.Model):
    _name = 'ems.examination.result'
    _description = 'ems_examination_result'
    _rec_name = 'reference'

    student_id = fields.Many2one('ems.student')
    class_id = fields.Many2one(related='student_id.class_id')
    reference = fields.Char(related='student_id.reference')
    exam_id = fields.Many2one('ems.examination', domain="[('class_id', '=', class_id)]")
    exam_type = fields.Selection(related='exam_id.exam_type')
    examination_result_line_ids = fields.One2many('ems.examination.result.line', 'examination_result_id')
    company_id = fields.Many2one('res.company' , default=lambda self: self.env.company.id)    
    present_days = fields.Integer(related='student_id.present_count')
    absent_days = fields.Integer(related='student_id.absent_count')
    leave_days = fields.Integer(related='student_id.leave_count')
    total_marks = fields.Integer(compute='_compute_total_marks', store=True)
    average_marks = fields.Float(compute='_compute_average_marks', store=True)
    result = fields.Char(compute='_compute_result', store=True)
    grade = fields.Char(compute='_compute_grade', store=True)
    exam_id = fields.Many2one('ems.examination')
    subject_id = fields.Many2one('ems.subject')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='State', default='draft')
    other_examination_result_line_ids = fields.One2many('ems.other.examination.result.line', 'examination_result_id')



    def action_mark_done(self):
        for record in self:
            record.state = 'done'

    def action_mark_cancel(self):
        for record in self:
            record.state = 'cancel'  

    @api.onchange('class_id')
    def _onchange_class_id(self):
        for rec in self:
            if rec.class_id:
                class_subjects = rec.class_id.class_line_ids
                rec.examination_result_line_ids = [(5, 0, 0)]
                new_lines = [(0, 0, {'subject_id': subject.subject_id.id}) for subject in class_subjects]
                rec.examination_result_line_ids = new_lines
            else:
                rec.examination_result_line_ids = False
            if rec.class_id:
                if rec.exam_type == 'other':
                    students = rec.class_id.student_ids
                    rec.other_examination_result_line_ids = [(5, 0, 0)]
                    rec.other_examination_result_line_ids = [(0, 0, {'student_id': student.id}) for student in students]
            else:
                rec.other_examination_result_line_ids = False

    @api.depends('examination_result_line_ids', 'exam_type')
    def _compute_total_marks(self):
        for rec in self:
            if rec.exam_type == 'mid-term':
                total_marks = sum(rec.examination_result_line_ids.mapped('mid_mark'))
                rec.total_marks = total_marks
            else:
                total_marks = sum(rec.examination_result_line_ids.mapped('final_mark'))
                rec.total_marks = total_marks
                
    @api.depends('examination_result_line_ids', 'exam_type')
    def _compute_total_marks(self):
        for rec in self:
            if rec.exam_type == 'mid-term':
                rec.total_marks = sum(rec.examination_result_line_ids.mapped('mid_mark'))
            elif rec.exam_type == 'final':
                rec.total_marks = sum(rec.examination_result_line_ids.mapped('final_mark')) + sum(rec.examination_result_line_ids.mapped('mid_mark'))

    @api.depends('examination_result_line_ids', 'total_marks', 'exam_type')
    def _compute_average_marks(self):
        for rec in self:
            subject_count = len(rec.examination_result_line_ids)
            if subject_count:
                rec.average_marks = rec.total_marks / subject_count
            else:
                rec.average_marks = 0.0

    @api.depends('exam_type', 'average_marks', 'total_marks')
    def _compute_result(self):
        for rec in self:
            if rec.exam_type == 'mid-term':
                if rec.average_marks >= 16 :
                    rec.result = 'Pass'
                else:
                    rec.result = 'Fail'
            elif rec.exam_type == 'final':
                if rec.average_marks < (40 / 100 * 100):
                    rec.result = 'Fail'
                else:
                    rec.result = 'Pass'
            else:
                rec.result = ''

    @api.depends('average_marks', 'exam_type')
    def _compute_grade(self):
        for rec in self:
            if rec.exam_type == 'mid-term':
                if 35 <= rec.average_marks <= 40:
                    rec.grade = 'A+'
                elif 30 <= rec.average_marks < 35:
                    rec.grade = 'A'
                elif 25 <= rec.average_marks < 30:
                    rec.grade = 'B'
                elif 20 <= rec.average_marks < 25:
                    rec.grade = 'C'
                elif 16 <= rec.average_marks < 20:
                    rec.grade = 'D'
                else:
                    rec.grade = 'F'
            elif rec.exam_type == 'final':
                if 90 <= rec.average_marks <= 100:
                    rec.grade = 'A+'
                elif 80 <= rec.average_marks < 90:
                    rec.grade = 'A'
                elif 70 <= rec.average_marks < 80:
                    rec.grade = 'B'
                elif 60 <= rec.average_marks < 70:
                    rec.grade = 'C'
                elif 40 <= rec.average_marks < 60:
                    rec.grade = 'D'
                else:
                    rec.grade = 'F'
    

    

class EmsExaminationResultLine(models.Model):
    _name = 'ems.examination.result.line'
    _description = 'ems_examination_result.line'

    subject_id = fields.Many2one('ems.subject')
    student_id = fields.Many2one('ems.student')
    max_mark = fields.Integer(related='subject_id.maximum_mark')
    min_mark = fields.Integer(related='subject_id.minimum_mark')
    mid_mark = fields.Integer()
    final_mark = fields.Integer()
    examination_result_id = fields.Many2one('ems.examination.result')
    exam_type = fields.Selection(related='examination_result_id.exam_type')
    total = fields.Integer(compute="_compute_total_of_marks")

    @api.depends('mid_mark', 'final_mark')
    def _compute_total_of_marks(self):
        for rec in self:
            rec.total = rec.mid_mark + rec.final_mark   

    @api.constrains('mid_mark', 'final_mark', 'examination_result_id')
    def _check_marks_range(self):
        for rec in self:
            if rec.examination_result_id:
                if rec.examination_result_id.exam_type == 'mid-term' and (rec.mid_mark < 0 or rec.mid_mark > 40):
                    raise ValidationError("Mid-term marks should be between 0 and 40.")
                if rec.examination_result_id.exam_type == 'final' and (rec.final_mark < 0 or rec.final_mark > 60):
                    raise ValidationError("Final marks should be between 0 and 60.")
                    



class EmsOtherExaminationResultLine(models.Model):
    _name = 'ems.other.examination.result.line'
    _description = 'ems_examination_result.line'

    student_id = fields.Many2one('ems.student')
    mark =  fields.Integer()
    examination_result_id = fields.Many2one('ems.examination.result')
    std_id = fields.Char(related='student_id.reference')