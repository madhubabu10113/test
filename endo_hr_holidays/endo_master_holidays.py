# -*- coding: utf-8 -*-
##############################################################################
#
#    Endosoft
#
##############################################################################

from openerp.osv import fields, osv
from datetime import date,timedelta,datetime
import time

class child_endoleaves(osv.osv):
    _name="child.endoleaves"
    _description="Child Endosoft Leaves"
    _columns={
	    'parentid':fields.integer('Parent ID'),
	    'name':fields.char('Name',size=50,required=True),
	    'leave_date':fields.date('Date',required=True),
	}
child_endoleaves()


class endo_master_hr_holidays(osv.osv):
    _name="endo.hr.master.holidays"
    _description="Master Holiday List"
    _columns={
	    'pid':fields.char('ID',size=3,required=True),
	    'name':fields.char('Name',size=60,required=True),
	    'leaves':fields.one2many('child.endoleaves','parentid','Leaves'),
	}
endo_master_hr_holidays()

