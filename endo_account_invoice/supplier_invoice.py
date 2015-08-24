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


class supplier_invoice(osv.osv):
	_inherit = 'account.invoice'

	_columns = {     
         
	}
	
supplier_invoice()
