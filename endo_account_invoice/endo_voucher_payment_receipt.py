# -*- coding: utf-8 -*-
##############################################################################
#
#    Endosoft
#
##############################################################################

#from openerp.addons.base_status.base_stage import base_stage
#import binascii
#import datetime

from openerp.addons.crm import crm
from openerp.osv import fields, osv
import time
from openerp import SUPERUSER_ID
import openerp.addons.decimal_precision as dp
#from openerp import tools
from openerp.tools.translate import _

class endo_account_invoice(osv.osv):

    _inherit = 'account.voucher'
    
endo_account_invoice()
