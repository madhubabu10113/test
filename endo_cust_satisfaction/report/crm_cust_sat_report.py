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
from datetime import datetime


class crm_cust_sat_report(osv.osv):
    """ License analysis"""
    _name = "cust.sat.report"
    _auto = False
    _description = "Customer Satisfaction Analysis"

    _columns = {

        'xinls': fields.integer('# of Scores', readonly=True),
        'name': fields.char('Name', size=128, required=True, select=True),
        'x_cs_date': fields.date('Date',required=True, select=True),
    	'x_cs_score' : fields.selection( [('happy', 'Happy'), ('neutral', 'Neutral'), ('monitoring', 'Monitoring'), ('unhappy', 'Unhappy'),     ('unknown', 'Unknown')], 'Satisfaction Score', required=True),
        'x_cs_note' : fields.char('Customer Notes'),
       
        }

    def init(self, cr):

        """
            Tickets analysis
            @param cr: the current row, from the database cursor
        """
        tools.drop_view_if_exists(cr, 'cust_sat_report')
        cr.execute("""
         CREATE OR REPLACE VIEW cust_sat_report AS (

                SELECT
                    inls.id as id,
                    inls.x_cs_date,
                    inls.x_cs_score,
                    inls.x_cs_note,
                    1 as xinls,
                    res.name

                    FROM
                    internal_lines inls,
                    res_partner res
                                        
                WHERE res.id=inls.internal_id
                AND inls.create_date = (SELECT MAX(create_date)
                                          FROM internal_lines inls1
                                          WHERE inls1.internal_id = inls.internal_id)
            )""")


    def unlink(self, cr, uid, ids, context=None):
        raise osv.except_osv(_('Error!'), _('You cannot delete any record from report section!'))
crm_cust_sat_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
