# -*- coding: utf-8 -*-
##############################################################################
#
# ENDOSOFT
#
##############################################################################

{
    'name': 'Global contacts repository/Address Book',
    'version': '1.0',
    'category': 'Tools',
    'description': """
This module gives you a quick view of your old address book, accessible from your home page.
You can track your suppliers, customers and other contacts.
""",
    'author': 'Endosoft',
    'website': 'http://openerp.com',
    'summary': 'Contacts, People and Companies',
    'depends': [
        'mail','contacts','crm'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/convert_to_lead.xml',
        'old_contacts_view.xml',
    ],
    'images': ['images/contacts.jpeg'],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
