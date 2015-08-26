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

class internal_lines(osv.osv):
    _name = "internal.lines"
    _columns = {
        'internal_id': fields.many2one('res.partner', 'Internal Notes', ondelete='cascade'),
        'x_cs_date': fields.date('Date',required=True, select=True),
	    #'x_cs_quarter': fields.selection( [('quart1', 'Quarter1'), ('quart2', 'Quarter2'), ('quart3', 'Quarter3'), ('quart4', 'Quarter4'),('annual','Annual')], 'Quarters'),
        'x_cs_score' : fields.selection( [('happy', 'Happy'), ('neutral', 'Neutral'), ('monitoring', 'Monitoring'), ('unhappy', 'Unhappy'), ('unknown', 'Unknown')], 'Satisfaction Score', required=True),
        'x_cs_note' : fields.char('Customer Notes'),
    }
internal_lines()

class res_partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
    	'internal_lines': fields.one2many('internal.lines','internal_id','Internal Note'),
    }
res_partner()


