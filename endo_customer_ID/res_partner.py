# -*- coding: utf-8 -*-
##############################################################################
#
# Endosoft
#
##############################################################################

from openerp.osv import fields,osv
from openerp.tools.translate import _
from datetime import date, datetime, timedelta
import time


class res_partner(osv.osv):
    _inherit = "res.partner"
    _columns = {
	       'parent_id': fields.many2one('res.partner', 'Related Company', select=True),
               'ref': fields.char('Account No.', size=64, select=1),
             }

    def create(self, cr, uid, vals, context=None):        
	print "vals",vals, '\n'
        if context is None:
            context = {}
#        force_company = vals['company_id']
#        valid_com = self.pool.get('res.partner').search(cr,uid,[('is_company','=','False')], context=context)
#        print "force_company id value",force_company
#	print "valid_com",valid_com
	print "is company", vals['is_company']
	print "condition value",vals.get('ref', '/')
        if vals.get('sequence_code', '/') == '/' and vals['is_company'] == True:
            print "vals.get is False then"
            vals['ref'] = self.pool.get('ir.sequence').next_by_code(
               cr, uid, 'res.partner', context=context) or '/' 
            print "Sequence Value",vals['ref']
	    return super(res_partner, self).create(cr, uid, vals, context=context)       
        else:
            print "else value return"
	    vals['ref']= ''
            return super(res_partner, self).create(cr, uid, vals, context=context)

    def onchange_address(self, cr, uid, ids, use_parent_address, parent_id, context=None):
        def value_or_id(val):
            """ return val or val.id if val is a browse record """
            return val if isinstance(val, (bool, int, long, float, basestring)) else val.id
        result = {}
        if parent_id:
            if ids:
                partner = self.browse(cr, uid, ids[0], context=context)
                if partner.parent_id and partner.parent_id.id != parent_id:
                    result['warning'] = {'title': _('Warning'),
                                         'message': _('Changing the company of a contact should only be done if it '
                                                      'was never correctly set. If an existing contact starts working for a new '
                                                      'company then a new contact should be created under that new '
                                                      'company. You can use the "Discard" button to abandon this change.')}
            parent = self.browse(cr, uid, parent_id, context=context)
            address_fields = self._address_fields(cr, uid, context=context)
            result['value'] = dict((key, value_or_id(parent[key])) for key in address_fields)

	    cr.execute("select ref from res_partner where id =%s ",(parent_id,))
	    ref_acc = cr.fetchone()[0]
	    print "ref_acc",ref_acc
            if ref_acc:
		return {'value':{'ref':ref_acc}}
	    else:
		return {'value':{'ref':''}}
        else:
            result['value'] = {'use_parent_address': False}
	    return {'value':{'ref':''}}
        return result


    """def onchange_zipcode(self, cr, uid, ids, parent_id, context=None):
	if parent_id :
	    cr.execute("select ref from res_partner where id =%s ",(parent_id,))
	    ref_acc = cr.fetchone()[0]
	    print "ref_acc",ref_acc
            if ref_acc:
		return {'value':{'ref':ref_acc}}
	    else:
		return {'value':{'ref':''}}
	else:
	    return {'value':{'ref':''}}"""

res_partner()
