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

    _columns = {
    	'db_server': fields.many2one('sys.info.db','Database server'),
        'x_technical_person': fields.many2one('hr.employee','Technical Person'),
        
    }
res_partner()
