# -*- coding: utf-8 -*-
from openerp.osv import fields,osv
from openerp import pooler
from openerp.tools.translate import _

class support_work_log(osv.osv_memory):

    def stop_work(self, cr, uid, ids, context=None):
        active_ids = context and context.get('active_ids', [])
        data =  self.browse(cr, uid, ids, context=context)[0]
        self.pool.get('crm.claim').stop_work(cr, uid, active_ids,data, context=context)
        return {'type': 'ir.actions.act_window_close'}


    _name="support.work.log"
    _description = " support Working Log"
    _columns =  {   
        'note':fields.text('Actions Taken',required="1"),
    }


support_work_log()
