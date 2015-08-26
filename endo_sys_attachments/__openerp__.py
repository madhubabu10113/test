# -*- coding: utf-8 -*-
##############################################################################
#
# Endosoft
#
##############################################################################


{
    'name': 'System Information',
    'version': '1.0',
    'category': 'crm',
    'sequence': 3,
    'summary': 'CRM, System Information, Licensce, Interfaces',
    'description': """This module will manage the installed system information """,
    'author': 'Endosoft',
    'website': 'http://www.endosoft.com',
    'depends': ['crm','product','sale'],
   
    'update_xml':[          
           
            'res_partner_view.xml',
            'ir/endo_attachments_view.xml',
            ],
    'demo': [],      
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
