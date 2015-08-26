# -*- coding: utf-8 -*-
##############################################################################
#
# Endosoft
#
##############################################################################


{
    'name': 'Crm System Information',
    'version': '1.0',
    'category': 'crm',
    'sequence': 3,
    'summary': 'CRM, System Information, Licensce, Interfaces',
    'description': """This module will manage the installed system information """,
    'author': 'Endosoft',
    'website': 'http://www.endosoft.com',
    'images': [],
    'depends': ['crm','product'],
    'data': ['security/ir.model.access.csv',
             'report/crm_license_report_view.xml',
             'views/endo_theme.xml',
            ],
    'update_xml':[
            'sys_info_view.xml',
            'res_partner_view.xml',
            ],
    'demo': [],
#    'js':['static/src/js/endo_sys_info.js'],
    'css':['static/src/css/endo_sys_info.css'],
#    'qweb': ['static/src/xml/endo_sys_info.xml'],
    'qweb' : ['static/src/xml/*.xml'],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
