# -*- coding: utf-8 -*-
##############################################################################
#
# Endosoft
#
##############################################################################

from openerp.osv import fields,osv
from collections import Counter
from openerp.tools.translate import _
from datetime import date, datetime, timedelta
import time


class res_partner(osv.osv):
    _inherit = 'res.partner'


    def onchange_zipcode(self, cr, uid, ids, x_zip, context=None):
#	len_zip = len(x_zip)
	if x_zip >=5:
	    x_zip = x_zip[0:5]
            if x_zip:
		cr.execute("select id from account_fiscal_position where name like " + "'%" + x_zip + "%'")	
		fis_all = cr.fetchall()
		if fis_all:
		    fis_pos = fis_all[0]
		    return {'value':{'property_account_position':fis_pos}}
		else:
		    return {'value':{'property_account_position':''}}
	    else:
		return {'value':{'property_account_position':''}}
	else:
	    return {'value':{'property_account_position':''}}

res_partner()


