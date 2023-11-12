# -*- coding: utf-8 -*-
{
    'name': "ems_attendance",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','ems-student'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'report/student_daily_attendance.xml',
        'report/student_monthly_attendance.xml',
        'views/ems_attendance_view.xml',
        'views/ems_class_room_view.xml',
        'views/ems_student_view.xml',
        'wizard/ems_attendance_report_wizard_view.xml',
        
    ],
}
