# -*- coding: utf-8 -*-
##############################################################################
#
#    Endosoft
#
##############################################################################

#from openerp.addons.base_status.base_stage import base_stage
#import binascii
from openerp.addons.sale import sale
from openerp.osv import fields, osv
import time
from openerp import SUPERUSER_ID
import openerp.addons.decimal_precision as dp
#from openerp import tools
from openerp.tools.translate import _

class endo_quotations(osv.osv):
    _inherit = 'sale.order'
	
    _columns = { 
				'client_order_ref':fields.char('Customer Reference', size=64), 
			}
endo_quotations()
