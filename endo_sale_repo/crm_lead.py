from openerp.addons.crm import crm
from openerp.osv import fields, osv
from datetime import date,timedelta,datetime
import time
from openerp import SUPERUSER_ID
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _


class crm_lead(osv.osv):
    _inherit='crm.lead'


    _columns = {
	        'x_sale_repo': fields.many2one('endo.sale.repo', 'Sales Reps'),
	}

crm_lead()
