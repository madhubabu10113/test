# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Customer Support Management',
    'version': '1.0',
    'category': 'Customer Relationship Management',
    'sequence': 5,
    'description': """

Manage Customer Support Tickets.
=================================
This application allows you to track your customers/suppliers tickets and grievances.

It is fully integrated with the email gateway so that you can create
automatically new tickets based on incoming emails.
    """,
    'author': 'Endosoft OpenERP Team',
    'website': 'http://www.endosoft.com',
    'depends': ['crm', 'crm_claim', 'portal_claim', 'fetchmail','endo_sys_info'],
    'data': [
        'crm_ticket_actions.xml',
        'security/ir.model.access.csv',
        'security/ticket_security.xml',
        'crm_partner_mail_history.xml',
        'res_partner_view.xml',

    ],
    # Endosoft
    'update_xml':[
                  'wizard/support_work_log.xml',
                  'crm_support_tickets_view.xml',
                  'crm_phonecall_view.xml',
                  'crm_support_faq_view.xml',
                  'tick_sequence.xml',
                  'crm_lead_view.xml',
                  ],
    'test': [],
    
#     qweb Added for hiding OpenERP announcement bar showing OPenERP is not supported. 
    'qweb' : [
        "static/src/xml/base.xml",],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
