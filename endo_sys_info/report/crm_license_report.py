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

from openerp.osv import fields,osv
from openerp import tools
from openerp.tools.translate import _

MONTHS = [
    ('01', 'January'),
    ('02', 'February'),
    ('03', 'March'),
    ('04', 'April'),
    ('05', 'May'),
    ('06', 'June'),
    ('07', 'July'),
    ('08', 'August'),
    ('09', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December')
]

class crm_license_report(osv.osv):
    """ License analysis"""
    _name = "crm.license.report"
    _auto = False
    _description = "CRM License Analysis"
#     _rec_name = 'license_name'

    _columns = {
                
        'license_id': fields.many2one('product.product','Product Installed',readonly=True),
        'comp_name': fields.char('Computer name', size=32,readonly=True),
        'exe_version':fields.many2one('sys.exe.version','Release #',readonly=True),
        'installed_month':fields.selection(MONTHS, 'Month of Installation', readonly=True),
        'installed_year':fields.char('Year of Installation', size=32,readonly=True),
        'installed_date': fields.char('Date of installation',readonly=True),
        'support_start': fields.char('Support Start Date',readonly=True),
        'support_end': fields.char('Support End Date',readonly=True),
        'deactive': fields.boolean('Deactive',readonly=True),
        'comments': fields.text('Comments',readonly=True),
        'room_name':  fields.many2one('sys.room','Room Name',readonly=True),
        'location': fields.many2one('res.partner','Location',readonly=True),
        'customer': fields.many2one('res.partner','Customer',readonly=True),
  }
    
    def init(self, cr):

        """
            License analysis
            @param cr: the current row, from the database cursor
        """
        tools.drop_view_if_exists(cr, 'crm_license_report')
        cr.execute("""
         CREATE OR REPLACE VIEW crm_license_report AS (
                SELECT
                    lc_line.id as id,
                    lc_line.name as license_id,
                    lc_line.comp_name as comp_name,
                    lc_line.exe_version as exe_version,
                    to_char(lc_line.installed_date, 'MM') as installed_month,
                    to_char(lc_line.installed_date, 'YYYY') as installed_year,
                    to_char(lc_line.installed_date, 'YYYY-MM-DD') as installed_date,
                    to_char(lc_line.support_start, 'YYYY-MM-DD') as support_start,
                    to_char(lc_line.support_end, 'YYYY-MM-DD') as support_end,
                    lc_line.deactive as deactive,
                    lc_line.comments as comments,
                    
                    rm.name as room_name,
                    rm.room_id as location,
                    cust.id as customer
                    FROM
                    licensce_lines lc_line
                    left join room_lines rm on lc_line.licenscee_id = rm.id
                    left join res_partner loc on rm.room_id = loc.id
                    left join location_line loc_line on loc.id = loc_line.name
                    left join res_partner cust on loc_line.part_loc_id = cust.id
                                        
                WHERE loc.active = 'true'
                
            )""")

    def unlink(self, cr, uid, ids, context=None):
        raise osv.except_osv(_('Error!'), _('You cannot delete any record from report section!'))
crm_license_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
