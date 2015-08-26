# -*- coding: utf-8 -*-
##############################################################################
#
#    Endosoft
#
##############################################################################

from openerp.addons.crm import crm
from openerp.osv import fields, osv
from datetime import date,timedelta,datetime
import time
from openerp import SUPERUSER_ID
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class endo_hr_holidays(osv.osv):

    def onchange_to_date(self, cr, uid, ids, date_to, date_from):
	result = {'value': {}}
	holiday_count = 0
	if (date_from and date_to) and (date_from > date_to):
            raise osv.except_osv(_('Warning!'),_('The start date must be anterior to the end date.'))
	DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        from_dt = datetime.strptime(date_from, DATETIME_FORMAT)
        to_dt = datetime.strptime(date_to, DATETIME_FORMAT)
	date_from = str(date_from)
	date_from = date_from[0:10]
	date_to = str(date_to)
	date_to = date_to[0:10]
	daygenerator = [from_dt + timedelta(x + 1) for x in xrange((to_dt - from_dt).days)]
	daygenerator += [from_dt + timedelta(0)]
	sum1 = sum(1 for day in daygenerator if day.weekday() < 5)
	cr.execute("select id from resource_resource where user_id=%s",(uid,))
	resource_id=cr.fetchone()[0]
	if resource_id:
		cr.execute("select leave_structure from hr_employee where resource_id=%s",(resource_id,))
		leave_structure=cr.fetchone()[0]
		if leave_structure:
			cr.execute("select count(*) from child_endoleaves where parentid=%s and leave_date>=%s and leave_date<=%s",(leave_structure,date_from,date_to,))
			holiday_count = cr.fetchone()[0]
	sum1 = sum1-holiday_count
        result['value']['number_of_days_temp'] = sum1
	return result

    _inherit = 'hr.holidays'
    
    _columns={
              'date_to': fields.datetime('End Date',readonly=True, states={'draft':[('readonly',False)], 'confirm':[('readonly',False)]}),
	      'date_from': fields.datetime('Start Date', readonly=True, states={'draft':[('readonly',False)], 'confirm':[('readonly',False)]}, select=True),
              }
endo_hr_holidays()

