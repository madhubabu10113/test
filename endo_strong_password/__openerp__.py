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
    'name': 'Strong Password',
    'version': '1.0',
    'category': 'Hidden',
    'sequence': 8,
    'description': """

Strong password enforcement.
=================================
This module makes users to enter strong password when reset password.
Password must be at least 6 characters long which contain at least 
one numeric digit, one uppercase, one lowercase letter and one Special Character.

    """,
    'author': 'Vinod Singh',
    'website': 'http://www.endosoft.com',
    'depends': ['base','auth_signup'],
    'data': [],
    # Endosoft
    'js': ['static/src/js/endo_auth_signup.js'],
    
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
