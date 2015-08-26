#from openerp.addons.base_status.base_state import base_state
#import crm
from datetime import datetime
from openerp.osv import fields, osv
#from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.tools.translate import _

class crm_phonecall(osv.osv):
    _inherit = 'crm.phonecall'
    
    _columns = {
         # Field claim_id is added....Vinod
        'claim_id': fields.many2one ('crm.claim', 'Support Ticket'),
        'name' : fields.text('Call Summary',required=True), #Inherited for incresing size
    }

 # Function added to convert logged call to Support ticket 
    def convert_support_ticket(self, cr, uid, ids, opportunity_summary=False, partner_id=False,  probability=0.0, context=None):
        partner = self.pool.get('res.partner')
        claim = self.pool.get('crm.claim')
        claim_dict = {}
        default_contact = False
        
        for call in self.browse(cr, uid, ids, context=context):
            parent = False
            if not partner_id:
                partner_id = call.partner_id and call.partner_id.id or False
            if partner_id:
                address_id = partner.address_get(cr, uid, [partner_id])['default']
                if address_id:
                    default_contact = partner.browse(cr, uid, address_id, context=context)
                
                parent = self.pool.get('res.partner').browse(cr, uid, partner_id).parent_id
                
            claim_id = claim.create(cr, uid, {
                            'name': opportunity_summary or call.name,
                   #         'planned_revenue': planned_revenue,
                            'user_id': call.user_id.id,
#                             'partner_id': partner_id or False,
                    #        'mobile': default_contact and default_contact.mobile,
                            'partner_id':parent and partner_id or False,
                            'customer':parent and parent.id or partner_id,
                            
                            'section_id': call.section_id and call.section_id.id or False,
                            'description': call.description or False,
                  #          'priority': call.priority,
                            'type_action': 'correction',
                            'partner_phone': call.partner_phone or False,
                            'email_from': default_contact and default_contact.email,
                        })
            vals = {
                    'partner_id': partner_id,
                    'claim_id' : claim_id,
            }
            self.write(cr, uid, [call.id], vals)
#            self.case_close(cr, uid, [call.id])
  #          claim.case_open(cr, uid, [opportunity_id])
            claim_dict[call.id] = claim_id
        return claim_dict
    
    def action_button_convert2claim(self, cr, uid, ids, context=None):
        """
        Convert a phonecall into an opp and then redirect to the opp view.

        :param list ids: list of calls ids to convert (typically contains a single id)
        :return dict: containing view information
        """
        if len(ids) != 1:
            raise osv.except_osv(_('Warning!'),_('It\'s only possible to convert one phonecall at a time.'))

        claim_dict = self.convert_support_ticket(cr, uid, ids, context=context)
        return True

crm_phonecall()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
