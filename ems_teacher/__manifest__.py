# -*- coding: utf-8 -*-
{
    'name': "ems_teacher",

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
    'depends': ['base','hr','ems-student'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/teacher_bedge.xml',
        'data/sequences.xml',
        'views/ems_teacher_view.xml',
        'views/ems_class_room_view.xml',
    ],
}
