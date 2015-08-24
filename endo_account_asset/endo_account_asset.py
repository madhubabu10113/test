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

class endo_account_asset(osv.osv):

    def set_to_close(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'close'}, context=context)

    _inherit = 'account.asset.asset'
    
    _columns={
              'purchase_value': fields.float('Cost Basis', required=True, readonly=True, states={'draft':[('readonly',False)]}),
              'endo_gross_value': fields.float('Purchase Value', readonly=True, states={'draft':[('readonly',False)]}),
              'tag' : fields.char("Asset Tag", size=32),
              'method_number': fields.integer('Asset Life(Years)', readonly=True, states={'draft':[('readonly',False)]}, help="The number of depreciations needed to depreciate your asset"),
              }
    _defaults = {
        'active':True,
        'name': lambda self, cr, uid, context: '/',
        }
    

    
endo_account_asset()


class account_asset_depreciation_line_inherit(osv.osv):
    _inherit = 'account.asset.depreciation.line'
    _description = 'Asset depreciation line'

    _columns = {
        'amount': fields.float('Current Year Depreciation', digits_compute=dp.get_precision('Account'), required=True),
        'depreciated_value': fields.float('Accumulated Depreciation', required=True),
    }
    
account_asset_depreciation_line_inherit()
