# -*- coding: utf-8 -*-
##############################################################################
#
# Endosoft
#
##############################################################################

from openerp.osv import fields,osv
from openerp.tools.translate import _
from datetime import date, datetime, timedelta
import time
#from datetime import datetime,date
#from dateutil.relativedelta import relativedelta


class res_partner(osv.osv):
    _inherit = 'res.partner'
    _columns = {
        'claims_ids': fields.one2many('crm.claim', 'partner_id', 'Support Tickets'),
        'claims_ids2': fields.one2many('crm.claim', 'x_customer', 'Support Tickets'),
        'cust_status':fields.text('Status', help="Provide the information about customer with its current information"\
                                  "e.g. Please make sure to provide excellent support as customer was unhappy"\
                                  "Or please pay attention as we are implementing new Hl& interfaces. etc."
                                  ),
                
        'ref': fields.char('Account No.', size=64, select=1),
    
    }
res_partner()