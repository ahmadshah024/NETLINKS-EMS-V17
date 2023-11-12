# -*- coding: utf-8 -*-

from odoo import models, fields, api

class EmsAttendanceWizard(models.TransientModel):
    _name = 'ems.attendance.report.wizard'
    _description = 'ems attendance report wizard'


    class_id = fields.Many2one('ems.class.room')
    start_date = fields.Date("From")
    end_date = fields.Date("To")
    company_id = fields.Many2one('res.company' , default=lambda self: self.env.company.id)

    def print_attendance_report(self):
        for rec in self:
            data = {
                'ids': rec.class_id.id,
                'model': 'ems.class.room',
                'form': rec.id,
            }
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<",data)
            return self.env.ref('ems_attendance.student_print_monthly_attendance').report_action(self, data=data)
            
# def print_attendance_report(self):
    #     # Collect all necessary data
    #     class_id = self.class_id.id
    #     start_date = self.start_date
    #     end_date = self.end_date

    #     # Fetch the attendance records for the selected class and date range
    #     attendance_records = self.env['ems.attendance'].search([
    #         ('class_id', '=', class_id),
    #         ('date', '>=', start_date),
    #         ('date', '<=', end_date),
    #     ])

    #     # Prepare data for the report
    #     report_data = []
    #     for attendance in attendance_records:
    #         report_data.append({
    #             'student_id': attendance.student_id.id,
    #             'name': attendance.student_id.name,
    #             'father_name': attendance.student_id.father_name,
    #             'present_days': attendance.present_days,
    #             'absent_days': attendance.absent_days,
    #             'leave_days': attendance.leave_days,
    #         })

    #     # Create a dictionary containing the data and pass it to the report
    #     data = {
    #         'wizard_data': {
    #             'class_id': class_id,
    #             'start_date': start_date,
    #             'end_date': end_date,
    #             'report_data': report_data,  # Include the attendance data
    #         },
    #     }

    #     return self.env.ref('ems_attendance.student_print_monthly_attendance').report_action(self, data=data)
    # def print_attendance_report(self):
    #     data = {
    #         'wizard_data': self.read()[0],
    #     }
    #     print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<",data)
    #     return self.env.ref('ems_attendance.student_print_monthly_attendance').report_action(self, data=data)

