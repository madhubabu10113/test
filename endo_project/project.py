# -*- coding: utf-8 -*-
from openerp import SUPERUSER_ID
from openerp import tools
from openerp.osv import fields, osv
#from openerp.addons.base_status.base_stage import base_stage

class db_server_licenses(osv.osv):
    _name = 'db.server.licenses'
    _description = 'Database Server Licenses'
    _columns = {
        'name' : fields.char('Name', size=32,required="1"),
        'description': fields.text('Description'),
    }

class ib_version(osv.osv):
    _name = 'ib.version'
    _description = 'IB Version'
    _columns = {
        'name' : fields.char('Name', size=32,required="1"),
        'description': fields.text('Description'),
    }


class project(osv.osv):
    _name = 'project.project'
    _inherit = 'project.project'
    _columns = {
#        'db_server_li':
        'partner_cust_id': fields.many2one('res.partner', 'Customer Project Manager', track_visibility='onchange'),
       # 'project_contact_lines' : fields.one2many('project.contact.lines', 'project_contact_id', 'Contacts'),
        'contacts': fields.many2many('res.partner', 'project_contact_rel', 'project_id', 'partner_id', 'Contacts',
            help="Project's contacts are contacts of the customer related to this project.", states={'close':[('readonly',True)], 'cancelled':[('readonly',True)]}),
        'prjct_lead_id': fields.many2one('hr.employee','Project Lead'),
        'ib_royality': fields.boolean('IB royalty paid'),
        'no_of_lice': fields.char('Number of licenses'),
        'db_server_id' : fields.many2one('db.server.licenses','Database License'),
        'ib_version_id': fields.many2one('ib.version','IB Version'),
        'project_desc': fields.html('Description'),
        'project_desc_pad': fields.html('Description'),
    }
#class project_contact_lines(osv.osv):
#    _name = "project.contact.lines"
#    _description = "Project Contact Lines"
#    _columns = {
#        'project_contact_id' : fields.many2one('project.project','Project ID',ondelete=True,required=True),
#        'contact_id' : fields.many2one
#        'name' :
#    }
class task(osv.osv):
    _inherit = "project.task"
    _columns = { 
        'wbs_id': fields.char('WBS ID',size=128),
        'is_risk' : fields.boolean('Risk'),
        'risk_probability': fields.selection([('4','Very Low'), ('3','Low'), ('2','Medium'), ('1','High'), ('0','Very High')], 'Risk Probability', select=True),
    }
