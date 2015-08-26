# -*- coding: utf-8 -*-
##############################################################################
#
# Endosoft
#
##############################################################################


{
    'name': 'Customer Score Information',
    'version': '1.0',
#    'category': 'crm',
    'sequence': 3,
    'summary': 'CRM, System Information, Customers, Satisfaction',
    'description': """This module will manage the Customer Satisfaction information """,
    'author': 'Endosoft',
    'website': 'http://www.endosoft.com',
    'images': [],
    'depends': ['crm'],
    'data': [
             'report/crm_cust_sat_report_view.xml',
              # 'dsys_info_data.xml'
            ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
