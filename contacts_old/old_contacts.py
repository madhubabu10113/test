# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp import tools
from openerp.tools.translate import _

class res_partner_old_contacts(osv.osv):
    _description = 'Old Parenter Contacts/Global contacts repository'
    _name = "res.partner.old.contacts"
    _rec_name='name'

    def _has_image(self, cr, uid, ids, name, args, context=None):
        result = {}
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = obj.image != False
        return result

    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
        return result


    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)


    def _compute_name_custom(self, cursor, uid, ids, fname, arg, context=None):
        res = {}
        for rec in self.read(cursor, uid, ids, ['firstname','middle_initial', 'lastname']):
            lastname=rec['lastname'] or ""
            name = (rec['firstname'] if rec['firstname'] else u"") + u" " +(rec['middle_initial'] if rec['middle_initial'] else u" ") + u" " +lastname
            res[rec['id']] = name.strip()
        return res

    def _write_name(self, cursor, uid, partner_id, field_name, field_value, arg, context=None):
        return self.write(cursor, uid, partner_id, {'lastname': field_value})


    def onchange_state(self, cr, uid, ids, state_id, context=None):
        if state_id:
            country_id = self.pool.get('res.country.state').browse(cr, uid, state_id, context).country_id.id
            return {'value':{'country_id':country_id}}
        return {}

    def convert_to_lead(self, cr, uid, ids, subject,context=None):
        obj_lead=self.pool.get('crm.lead')
        vals={}
        for data in self.browse(cr, uid, ids, context):
            vals={
                'name': subject,
                'partner_name':data.company_name or '',
                'firstname':data.firstname or '',
                'lastname': data.lastname or '',
                'title': data.title.id or '',
                'street': data.address or '',
                'street2': data.address2 or '',
                'city': data.city or '',
                'zip': data.zip or '',
                'state_id': data.state_id.id or '',
                'country_id': data.country_id.id or '',
                'email_from': data.email or '',
                'function': data.job_position or '',
#                'website': data.website or '',
                'phone': data.phone or '',
#                'other_phone': data.other_phone or '',
                'mobile': data.mobile or '',
                'fax': data.fax or '',
                'referred': data.source or '',

                'user_id': data.user_id.id or '',
                'section_id': data.section_id.id or '',
                'categ_ids': [(6,0,[x.id for x in data.category_id] or [])],

                'description': data.comment or '',

            }
        res_id=obj_lead.create(cr, uid, vals)
        self.unlink(cr, uid, ids, context=context)
        #view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'contacts_old', 'view_partner_old_contacts_kanban')
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'crm', 'crm_case_form_view_leads')

        view_id = view_ref and view_ref[1] or False,
        return {
            'name': _('Leads'),
            'view_type': 'form',
            'view_id': view_id,
            'res_id':res_id,
            'view_mode': 'form',
            'res_model': 'crm.lead',
            'type': 'ir.actions.act_window',
            }

    _columns = {
        'name': fields.function(_compute_name_custom, string="Name",type="char", store=True,select=True, readonly=True,fnct_inv=_write_name),
        'image': fields.binary("Image",help="This field holds the image used as image for the product, limited to 1024x1024px."),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,string="Medium-sized image", type="binary", multi="_get_image",
                        store={'res.partner.old.contacts': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),}),
        'image_small': fields.function(_get_image, fnct_inv=_set_image,string="Small-sized image", type="binary", multi="_get_image",
                        store={'res.partner.old.contacts': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),}),
        'has_image': fields.function(_has_image, type="boolean"),
        'color': fields.integer('Color Index'),

        'firstname': fields.char("Firstname", size=128),
        'middle_initial': fields.char('MI',size=128),
        'lastname' : fields.char('Lastname',size=128,required=True),
        'company_name': fields.char('Company Name',size=128),
        'title': fields.many2one('res.partner.title', 'Title'),
        'job_position': fields.char('Job Position', size=128),
        'address': fields.char('Address', size=128),
        'address2': fields.char('Address2', size=128),
        'zip': fields.char('Zip', change_default=True, size=24),
        'city': fields.char('City', size=128),
        'state_id': fields.many2one("res.country.state", 'State'),
        'country_id': fields.many2one('res.country', 'Country'),
        'website': fields.char('Website', size=64, help="Website of Partner or Company"),
        'department': fields.char('Department',size=128),
        
        'phone': fields.char('Phone', size=64),
        'other_phone': fields.char('Other Phone', size=64),
        'work_phone': fields.char('Work Phone', size=64),
        'mobile': fields.char('Mobile', size=64),
        'fax': fields.char('Fax', size=64),
        'email': fields.char('Email', size=240),
        
        'source':fields.char('Source/ Reference',size=64),
        'user_id': fields.many2one('res.users', 'Salesperson', select=True, track_visibility='onchange'),
        'section_id': fields.many2one('crm.case.section', 'Sales Team',
                        select=True, track_visibility='onchange', help='When sending mails, the default email address is taken from the sales team.'),
        'comment': fields.text('Notes'),
        'date_created':fields.date('Date of entry'),
        'category_id':fields.many2many('crm.case.categ', 'res_partner_old_contacts_category_rel', 'res_old_id', 'category_id', 'Categories', \
            domain="['|',('section_id','=',section_id),('section_id','=',False), ('object_id.model', '=', 'res.partner.old.contacts')]"),
    }
    _defaults={ 
        'date_created':fields.date.context_today,
}
    


