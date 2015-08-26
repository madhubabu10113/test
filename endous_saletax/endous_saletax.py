#from openerp.addons.base_status.base_state import base_state
#import crm
# from datetime import datetime
from openerp.osv import fields, osv
#from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
# from openerp.tools.translate import _


class company(osv.osv):
    _inherit = 'res.company'
    _columns = {
        'us_taxation': fields.boolean(
            'US Taxation',
            help="If checked, Only taxes with customer's fiscal position "\
                 "will be applied while creating Sale order."\
                 "Taxes with product will not be included in sale order lines."),
    }
    
company()

class account_fiscal_position(osv.osv):
    _inherit = 'account.fiscal.position'

    def map_tax(self, cr, uid, fposition_id, taxes, context=None):
        res = super(account_fiscal_position, self).map_tax(cr, uid, fposition_id, taxes, context)
        comp_id = self.pool.get('res.company')._company_default_get(cr, uid, 'sale.shop', context)
        if comp_id:
            us_tax = self.pool.get('res.company').browse(cr,uid,comp_id).us_taxation
            if us_tax:
                if not fposition_id:
                    res = []
                else:
                    result = set()
                    for tax in fposition_id.tax_ids:
                        if tax.tax_dest_id:
                            result.add(tax.tax_dest_id.id)
                        else:
                            result.add(tax.tax_src_id.id)
                    res = list(result)
        return res

account_fiscal_position()












#===============================================================================
# class account_tax(osv.osv):
#     _inherit = 'account.tax'
#     _columns={'zip': fields.char('Zip', size=24),}
# account_tax()
# class sale_order_line(osv.osv):
# 
#     _inherit = 'sale.order.line'
#     
#     def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
#             uom=False, qty_uos=0, uos=False, name='', partner_id=False,
#             lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
#         
#         res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty,
#             uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
#             lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)
#         if partner_id:
#             pzip = self.pool.get('res.partner').browse(cr,uid,partner_id).zip
#             if pzip:
#                 tax_ids = self.pool.get('account.tax').search(cr, uid, [('zip','=',pzip)], context=None)
#                 if tax_ids:
#                     res['value']['tax_id'] = tax_ids
#         return res
# sale_order_line()
#===============================================================================
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: