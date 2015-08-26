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
    'name': 'ENDOSOFT Leave Management',
    'version': '1.5',
    'author': 'OpenERP SA',
    'category': 'Human Resources',
    'sequence': 27,
    'summary': 'Holidays, Allocation and Leave Requests',
    'website': 'http://www.openerp.com',
    'description': """
Manage leaves and allocation requests
=====================================

This application controls the holiday schedule of your company. It allows employees to request holidays. Then, managers can review requests for holidays and approve or reject them. This way you can control the overall holiday planning for the company or department.

You can configure several kinds of leaves (sickness, holidays, paid days, ...) and allocate leaves to an employee or department quickly using allocation requests. An employee can also make a request for more days off by making a new Allocation. It will increase the total of available days for that leave type (if the request is accepted).

You can keep track of leaves in different ways by following reports: 

* Leaves Summary
* Leaves by Department
* Leaves Analysis

A synchronization with an internal agenda (Meetings of the CRM module) is also possible in order to automatically create a meeting when a holiday request is accepted by setting up a type of meeting in Leave Type.
""",
    'depends': ['hr','hr_holidays',],
    'data': [
        'endo_hr_employee_view.xml',
        'endo_hr_holidays_view.xml',
        'endo_master_holidays_view.xml',        
        ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
