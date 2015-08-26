# -*- coding: utf-8 -*-
##############################################################################
#
#    Endosoft
#
##############################################################################

#from openerp.addons.base_status.base_stage import base_stage
#import binascii
from openerp.addons.crm import crm
from openerp.osv import fields, osv
import time
from openerp import SUPERUSER_ID
#from openerp import tools
from openerp.tools.translate import _

class crm_support_faq(osv.osv):
    _name = 'crm.support.faq'
    
    def create(self, cr, uid, vals, context=None):
        if ('name' not in vals) or (vals.get('name')=='/') or (vals.get('name')==''):
            seq_obj_name =  'crm.support.faq'
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, seq_obj_name)
        new_id = super(crm_support_faq, self).create(cr, uid, vals, context)
        return new_id
    
    _columns={
              'name': fields.char('FAQ No.', size=64, readonly=True),
              'faq_title': fields.char('FAQ Title', size=128, required=True),
             # 'description': fields.html('Description'),
              'description': fields.text('Description'),
              'categ_id': fields.many2one('crm.case.categ', 'Category', \
                            domain="[('object_id.model', '=', 'crm.claim')]"),
#               'tick_ids':fields.many2many('crm.claim', 'crm_ticket_faq_rel', 'faq_id','tick_id', string='Related Tickets',),
              'tick_ids':fields.one2many('crm.claim', 'x_ref_faq', 'Referenced by Tickets', readonly=True),
              'owner_tick':fields.many2one('crm.claim',"Owner Ticket", readonly=True),
#               'sub_faqs':fields.related('owner_tick', 'faq_ids', type="many2many", relation="crm.support.faq", string="Substitute FAQs", readonly=True),
              'resolution': fields.text('Resolution'),
              'type_action': fields.selection([('correction','Corrective Action'),('prevention','Preventive Action')], 'Action Type'),
              'active': fields.boolean('Active', help="By unchecking the active field you can disable this FAQ without deleting it.",store=True),
              }
    _defaults = {
        'active':True,
        'name': lambda self, cr, uid, context: '/',
        }
    
    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default.update({
            'name': self.pool.get('ir.sequence').get(cr, uid, 'crm.support.faq') or '/',
            'tick_ids':[],
            'owner_tick':False,
        })
        return super(crm_support_faq, self).copy(cr, uid, id, default, context)
    
crm_support_faq()
