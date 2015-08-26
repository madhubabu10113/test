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

class endo_sale_repo(osv.osv):

    _name = 'endo.sale.repo'
    _description="Sales Reps- Distributors"
    
    _columns={
#	        'reps_id':fields.char('ID'),
		'name':fields.char('Sales Reps', size=64, required=True),
              }
endo_sale_repo()

