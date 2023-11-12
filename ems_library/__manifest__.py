# -*- coding: utf-8 -*-
{
    'name': "ems_library",

    'summary': """
        ems_library""",

    'description': """
     ems_library
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'ems-student'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/ems_library_books_views.xml',
        'views/ems_library_views.xml',
        'data/sequences.xml',

    ],
}
