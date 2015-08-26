# -*- coding: utf-8 -*-
##############################################################################
#
# Endosoft
#
##############################################################################


{
    'name': 'Endo Internal Notes',
    'version': '1.0',
#    'category': 'crm',
    'sequence': 3,
    'summary': 'CRM, Internal Notes Information',
    'description': """This module will give the information about Year base Customer Satisfaction """,
    'author': 'Endosoft',
    'website': 'http://www.endosoft.com',
    'depends': ['base'],
   
    'update_xml':[          
           
            'res_partner_view.xml',
            ],
#    'demo': [],   
#    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
