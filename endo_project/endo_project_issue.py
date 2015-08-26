# -*- coding: utf-8 -*-
##############################################################################
#
#    Endosoft
#
##############################################################################

#from openerp.addons.base_status.base_stage import base_stage
#import binascii
from openerp.addons.project_issue import project_issue
from openerp.osv import fields, osv
import time
from openerp import SUPERUSER_ID
import openerp.addons.decimal_precision as dp
#from openerp import tools
from openerp.tools.translate import _

class endo_project_issue(osv.osv):
    _inherit = 'project.issue'
    
    _columns={
              'x_res_issue': fields.text('Private Note'),
              }
    _defaults = {
        'active':True,
        'name': lambda self, cr, uid, context: '/',
        }
    

    
endo_project_issue()
