# -*- coding: utf-8 -*-
{
    'name': "ems_timetable",

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
    'depends': ['base','ems-student','ems_teacher'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        "report/report.xml",
        'report/timetable_report.xml',
        'report/exam_timetable_report.xml',
        'data/sequences.xml',
        'views/ems_timetable_view.xml',
        'views/ems_exam_timetable_view.xml',
        'views/ems_subject_view.xml',
        'views/ems_subject_view.xml',
        'views/ems_class_room_view.xml',
        'views/ems_period_view.xml',
        'views/ems_day_view.xml',
        'views/ems_teacher_view.xml',
        'views/ems_teacher_timetable_view.xml',
        


    ],
}
