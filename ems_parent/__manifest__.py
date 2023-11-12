# -*- coding: utf-8 -*-
{
    'name': "parent",

    'summary': """
       Ems parent""",

    'description': """
        Ems parent
    """,

    'author': "Netlinks",
    'website': "https://www.Nenlinks LTD.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/ems_parent_views.xml',
        
    ],
}
