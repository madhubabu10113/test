# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

class convert_to_lead(osv.osv_memory):
    _name='convert.to.lead'
    _description = 'Convert the old contacts to Lead'

    def action_create_lead(self, cr, uid, ids, context=None):
        """Convert old contact to lead"""
        if context is None:
            context = {}
        data = self.browse(cr, uid, ids, context=context)[0]
        old_contact_ids = context.get('active_ids', [])
        return self.pool.get('res.partner.old.contacts').convert_to_lead(cr, uid,old_contact_ids,data.name, context=context)

    _columns ={
        'name': fields.char('Subject',required=True),
    }
