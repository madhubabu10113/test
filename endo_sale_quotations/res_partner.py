# -*- coding: utf-8 -*-
##############################################################################
#
# Endosoft
#
##############################################################################

from openerp.osv import fields,osv
from collections import Counter
from openerp.tools.translate import _
from datetime import date, datetime, timedelta
import time


class res_partner(osv.osv):
 
    _inherit ="crm.lead"

    _columns = {
       'partner_id': fields.many2one('res.partner', 'Partner', ondelete='set null', track_visibility='onchange',
            select=True, help="Linked partner (optional). Usually created when converting the lead."),
    }

    def on_change_partner(self, cr, uid, ids, partner_id, context=None):
        values = {}
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
            values = {
                'partner_name' : partner.name,
                'street' : partner.street,
                'street2' : partner.street2,
                'city' : partner.city,
                'state_id' : partner.state_id and partner.state_id.id or False,
                'country_id' : partner.country_id and partner.country_id.id or False,
                'email_from' : partner.email,
                'phone' : partner.phone,
                'mobile' : partner.mobile,
                'fax' : partner.fax,
                'zip': partner.zip,
            }
        return {'value' : values}


res_partner()
