from odoo import models, api

class EmsAttendanceMonthlyReport(models.AbstractModel):
    _name = 'report.ems_attendance.print_student_monthly_attendance'
    _description = 'ems attendance monthly report'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name('ems_attendance.student_print_monthly_attendance')
        wizard_id = self.env['ems.attendance.report.wizard'].browse(data.get('form'))
        class_id = wizard_id.class_id
        start_date = wizard_id.start_date
        end_date = wizard_id.end_date
        if class_id and start_date and end_date:
            # Fetch the attendance records for the selected class and date range
            attendance_records = self.env['ems.attendance'].search([
                ('class_id', '=', class_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
            ])

            # Prepare data for the report
            report_data = []
            for attendance in attendance_records:
                attendance_line_data = []
                for line in attendance.attendance_line_ids:
                    attendance_line_data.append({
                        'student_id': line.student_id.id,
                        'student_reference': line.student_id.reference,
                        'name': line.student_id.name,
                        'father_name': line.student_id.father_name,
                        'present_days': line.is_present,
                        'absent_days': line.is_absent,
                        'leave_days': line.is_leave,
                    })

                report_data.append({
                    'attendance_date': attendance.date,
                    'class_id': attendance.class_id.name,
                    'attendance_lines': attendance_line_data,
                })

            # Calculate totals for each student within the date range
            student_totals = {}
            for record in report_data:
                for line in record['attendance_lines']:
                    student_id = line['student_id']
                    if student_id not in student_totals:
                        student_totals[student_id] = {
                            'student_id': student_id,
                            'student_reference': line['student_reference'],
                            'name': line['name'],
                            'father_name': line['father_name'],
                            'present_days': 0,
                            'absent_days': 0,
                            'leave_days': 0,
                        }
                    student_totals[student_id]['present_days'] += line['present_days']
                    student_totals[student_id]['absent_days'] += line['absent_days']
                    student_totals[student_id]['leave_days'] += line['leave_days']

            # Convert student_totals dictionary to a list
            student_totals_list = list(student_totals.values())

            return {
                'docs': wizard_id,
                'doc_ids': data,
                'doc_model': report.model,
                'data': student_totals_list,  # Use the calculated student_totals_list
                'class_id': class_id,
            }

    # @api.model
    # def _get_report_values(self, docids, data=None):
    #     report = self.env['ir.actions.report']._get_report_from_name('ems_attendance.student_print_monthly_attendance')
    #     wizard_id = self.env['ems.attendance.report.wizard'].browse(data.get('form'))
    #     class_id = wizard_id.class_id
    #     start_date = wizard_id.start_date
    #     end_date = wizard_id.end_date
    #     if class_id and start_date and end_date:
    #         # Fetch the attendance records for the selected class and date range
    #         attendance_records = self.env['ems.attendance'].search([
    #         ('class_id', '=', class_id.id),
    #         ('date', '>=', start_date),
    #         ('date', '<=', end_date),
    #     ])

    #     # Prepare data for the report
    #     report_data = []
    #     for attendance in attendance_records:
    #         attendance_line_data = []
    #         for line in attendance.attendance_line_ids:
    #             attendance_line_data.append({
    #                 'student_id': line.student_id.id,
    #                 'name': line.student_id.name,
    #                 'father_name': line.student_id.father_name,
    #                 'present_days': line.is_present,
    #                 'absent_days': line.is_absent,
    #                 'leave_days': line.is_leave,
    #             })

    #         report_data.append({
    #             'attendance_date': attendance.date,
    #             'class_id': attendance.class_id.name,
    #             'attendance_lines': attendance_line_data,
    #         })
  
    #     print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4",attendance_line_data,'\n\n')
    #     return {
    #         'docs': wizard_id,
    #         'doc_ids': data,
    #         'doc_model': report.model,
    #         'data': report_data,
    #         'class_id': class_id,
    #     }
    
    
        # Retrieve the data including attendance records from the wizard
        # wizard_data = data.get('wizard_data', {})
        # class_id = wizard_data.get('class_id', False)
        # start_date = wizard_data.get('start_date', False)
        # end_date = wizard_data.get('end_date', False)
        # report_data = wizard_data.get('report_data', [])
        # if class_id and start_date and end_date:
        #     # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",report_data)
        #     # You can use report_data as needed for your report template

        #     return {
        #         'data': report_data,
        #     }
        # else:
        #     # Handle the case when class_id, start_date, or end_date is missing
        #     # print("##############################################################")
        #     return {}
    # @api.model
    # def _get_report_values(self, docids, data=None):
    #     # Retrieve class_id, start_date, and end_date from the data dictionary
    #     class_id = data.get('wizard_data', {}).get('class_id', False)
    #     start_date = data.get('wizard_data', {}).get('start_date', False)
    #     end_date = data.get('wizard_data', {}).get('end_date', False)

    #     if class_id and start_date and end_date:
    #         # Fetch the attendance records for the selected class and date range
    #         attendance_records = self.env['ems.attendance'].search([
    #             ('class_id', '=', class_id),
    #             ('date', '>=', start_date),
    #             ('date', '<=', end_date),
    #         ])

    #         # Prepare data for the report
    #         report_data = []
    #         for attendance in attendance_records:
    #             report_data.append({
    #                 'student_id': attendance.student_id.id,
    #                 'name': attendance.student_id.name,
    #                 'father_name': attendance.student_id.father_name,
    #                 'present_days': attendance.present_days,
    #                 'absent_days': attendance.absent_days,
    #                 'leave_days': attendance.leave_days,
    #             })

    #         return {
    #             'data': report_data
    #         }
    #     else:
    #         # Handle the case when class_id, start_date, or end_date is missing
    #         return {}

    
    # @api.model
    # def _get_report_values(self, docids, data=None):
    #     attendance_records = self.env['ems.attendance'].search([
    #             ('class_id', '=', class_id),
    #             ('date', '>=', start_date),
    #             ('date', '<=', end_date),
    #         ])
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

    #     return {
    #         'data': report_data
    #     }
    #     # return {
    #     #     'data': data.get('wizard_data')
    #     # }
    