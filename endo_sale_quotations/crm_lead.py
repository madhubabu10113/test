#from openerp.addons.base_status.base_state import base_state
#import crm
from datetime import datetime
from openerp.osv import fields, osv
from openerp.tools.translate import _

class crm_lead(osv.osv):
    _inherit = 'crm.lead'
    
    _columns = {
        'x_lead_next_action_date': fields.date('Next Action Date',required=True),
    }

crm_lead()

