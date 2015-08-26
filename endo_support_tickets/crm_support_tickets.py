# -*- coding: utf-8 -*-
##############################################################################
#
#    Endosoft
#
##############################################################################

#from openerp.addons.base_status.base_stage import base_stage
#import binascii
from lxml import etree
from datetime import datetime, timedelta
from openerp.addons.crm import crm
from openerp.osv import fields, osv, orm
import time
from openerp import SUPERUSER_ID
#from openerp import tools
from openerp.tools.translate import _
#from openerp.tools import html2plaintext

class crm_ticket_priority(osv.osv):
    _name="crm.ticket.priority"
    
    def _check_default(self, cr, uid, ids, context=None):
        all_ids = self.search(cr, uid, [])
        count = 0
        for pri in self.browse(cr, uid, all_ids, context=context):
            if pri.default:
                count = count + 1
        if count > 1:
            return False
        return True
    
    _columns={'name':fields.char('Priority name', size=128, required=True),
              #'tot_alert':fields.integer('Total alerts', help="Enter the number that how many times alert should be sent for this priority."),
              'desc':fields.text('Description'),
  #            'durations':fields.one2many('crm.ticketpriority.delays','priority_id','Alert Intervals'),
              'interval_number': fields.integer('Interval Number',help="Repeat every x."),
              'interval_type': fields.selection( [('minutes', 'Minutes'),
                                                  ('hours', 'Hours'), ('work_days','Work Days'), ('days', 'Days'),('weeks', 'Weeks'), ('months', 'Months')], 'Interval Unit'),
              'numberemail': fields.integer('Number of e-mails', help='How many times you want to send alert e-mails to the ticket owner for this priority,\na negative number indicates no limit.'),
              'default':fields.boolean('Dafault', help="Check this if you want to make this priority as Default priority of new support tickets.")
              }
    _defaults={
               'interval_number':lambda self, cr, uid, context: 1,
               'numberemail':lambda self, cr, uid, context: 1,
               'interval_type':'days',
               'default':False,
               }
    
    _constraints = [
        (_check_default,
            'Please check priorities, Only one or atleast one priority should be set as default.!',
            ['default']),]
    
crm_ticket_priority()

#===============================================================================
# #     Configuration for default responsible in support ticket
#===============================================================================

class crm_ticket_mgr(osv.osv):
    _name="crm.ticket.mgr"
    _columns = {
			  'name':fields.text('Note'),
              'company_id': fields.many2one('res.company', 'Company', select=1, required=True),
			  'default_mgrs': fields.many2many('res.users', 'defmgr_user_rel', 'defmgr_tbl_id', 'user_id', 'Support Engineers',help="Support Engineers will get alert mails for unassigned tickets per company."),
	}
    _sql_constraints = [
        ('comp_uniq', 'unique(company_id)', 'Only one record can be created for each company!'),
    ]
    
crm_ticket_mgr()

#===============================================================================
# Class for removing tracking in message thread for Expected revenue from Lead/Opportunity
#===============================================================================

class crm_lead(osv.osv):
    
    _inherit="crm.lead"
    _columns = {
                 'planned_revenue': fields.float('Expected Revenue',),
                 }

crm_lead()



class crm_support_tickets(osv.osv):

    """ crm_support_tickets
    """
    _inherit="crm.claim"
    _description = "Support Tickets"
    _rec_name = "x_tick_id"
    _order = "date desc"
    _table = "crm_claim"


    def create(self, cr, uid, vals, context=None):
        pri_id = vals.get('priority',False)
        x_cron_id=False
        if pri_id:
            priority = self.pool.get('crm.ticket.priority').browse(cr, uid, pri_id, context=None)
            svals = {
                 'name':"Send E-mail alert to user for Ticket: ",
                 'interval_number': priority.interval_number or 0,
                 'interval_type': priority.interval_type or 'days',
                 'numbercall': priority.numberemail or 0,
                 'model':'crm.claim',
                 'priority':1,
                 'active':True,'doall':False,
                 'function':'_run_alertmail',
                 'args':'()',
                 'user_id':uid,
          #       'nextcall':
                 }
            x_cron_id = self.pool.get('ir.cron').create(cr,SUPERUSER_ID,svals,context=None)
            vals.update({'x_cron_id':x_cron_id,})
        if ('x_tick_id' not in vals) or (vals.get('x_tick_id')=='/') or (vals.get('x_tick_id')==''):
            seq_obj_name =  'crm.support.tickets'
            vals['x_tick_id'] = self.pool.get('ir.sequence').get(cr, uid, seq_obj_name)
        if vals.get('partner_id'):
            vals['message_follower_ids'] = [(4, vals.get('partner_id'))]
        new_id = super(crm_support_tickets, self).create(cr, uid, vals, context)
        if pri_id and x_cron_id:
            self.pool.get('ir.cron').write(cr,SUPERUSER_ID,[x_cron_id],{'args':'('+str(new_id)+',)', 'name': "Send E-mail alert to user for Ticket: " + str(vals.get('x_tick_id')),},context=None)
        self.send_ack_email(cr, uid, [new_id], context)
        
#         Added for immediate alert Mail sending
        self.send_alert_email(cr, uid, [new_id], context)
        return new_id



    def _faq(self, cursor, user, ids, name, arg, context=None):
        res = {}
#         faq_obj= self.pool.get('crm_support_faq')
        for tick in self.browse(cursor, user, ids, context=context):
            res[tick.id] = False
            if tick.x_faq_id:
                res[tick.id] = True
        return res

    def _get_color_index(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for tick in self.browse(cursor, user, ids, context=context):
            res[tick.id] = 0
            if tick.x_escalate_to:
                res[tick.id] = 9
        return res

    def _res_portal(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for tick in self.browse(cursor, user, ids, context=context):
            res[tick.id] = tick.resolution
        return res


    def _time_spend(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if context is None:
            context = {}
        for time_spend in self.browse(cr, uid, ids, context=context):
            diff_total = datetime.now() - datetime.now()
            if not time_spend.work_log_lines:
                return res
            for line in time_spend.work_log_lines:
                if len(time_spend.work_log_lines) == 1 and not line.note:
                    return res
                cdate= datetime.strptime(line.create_date, '%Y-%m-%d %H:%M:%S')
                wdate= datetime.strptime(line.write_date, '%Y-%m-%d %H:%M:%S')
                diff_total += (wdate - cdate)
            str(diff_total)
            res[time_spend.id] =str(timedelta(seconds=diff_total.seconds))
        return res


    _columns = {
        'name': fields.char('Ticket Title', size=128, required=True),
        'date': fields.datetime('Ticket Date', select=True),

       #Endosoft
        'x_color':fields.function(_get_color_index, string='Color Index',type='integer'),
        'user_id': fields.many2one('res.users', 'Responsible', track_visibility='onchange',),
        'x_tick_id':fields.char('Ticket No.', size=64, readonly=True),
        'x_escalate_to': fields.many2one('res.users', 'Escalate to', track_visibility='onchange',),

        'faq':fields.function(_faq, string='FAQ',type='boolean', help="It indicates that an invoice has been paid."),
        'x_customer': fields.many2one('res.partner', 'Customer', domain=[('parent_id','=',False)]),
        # Partner ID is now used as contact person.
        'partner_id': fields.many2one('res.partner', 'Contact Person', domain=['!',('parent_id','=',False),('x_location','=',False)]),      
        'x_location': fields.many2one('res.partner', 'Location', domain=[('x_location','=',True)]),
        'x_room': fields.many2one('room.lines', 'Room'),
        'x_license_id': fields.many2one('licensce.lines','License'),
        'x_cron_id':fields.many2one('ir.cron', 'Scheduler for alert E-mails'),
        'x_acknowledged':fields.boolean('Acknowledged to customer'),
        'priority':fields.many2one('crm.ticket.priority', 'Priority', required=True),
        'x_opportunity_id': fields.many2one ('crm.lead', 'Lead/Opportunity'),
        'x_faq_id': fields.many2one ('crm.support.faq', 'Ticket FAQ', readonly=True),
        'x_ref_faq':fields.many2one ('crm.support.faq', 'Reference FAQ', readonly=False),
        
        'resolution2': fields.function(_res_portal, type='text', string='Resolution'),
        'work_log_lines': fields.one2many('work.log.lines','ticket_log_id','Log'),
        'is_working' : fields.boolean('Is Working'),
        'time_spend' : fields.function(_time_spend, string='Time Worked',type="char",store=True),       
        'x_cir': fields.text('Customer Information Request'),
    }

    def _find_priority(self, cr, uid, context=None):
        """Finds id for case object"""
        context = context or {}
        object_id = context.get('object_id', False)
        n_ids = self.pool.get('crm.ticket.priority').search(cr, uid, ['|',('id', '=', object_id),('name', '=', 'Normal')])
        ids = self.pool.get('crm.ticket.priority').search(cr, uid, [('default', '=', True)])
        return ids and ids[0] or (n_ids and n_ids[0] or False)
    

    _defaults = {
        'x_tick_id': lambda self, cr, uid, context: '/',
        'x_color': 0,
#         'faq':False,
        'x_acknowledged':False,
        'priority' : _find_priority,
        'user_id':False,
        }

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default.update({
            'x_tick_id': self.pool.get('ir.sequence').get(cr, uid, 'crm.support.tickets') or '/',
            'x_acknowledged' : False,
            'date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'x_opportunity_id':False,
            'x_faq_id':False,
#             'faq_ids':[],
            'x_cron_id':False,
            'x_escalate_to':False
        })
        return super(crm_support_tickets, self).copy(cr, uid, id, default, context)

    def unlink(self, cr, uid, ids, context=None):
        """ Overwrite unlink method of ticket to delete its email scheduler upon ticket deletion """
        for tick in self.browse(cr, uid, ids, context):
            if tick.x_cron_id:
                self.pool.get('ir.cron').unlink(cr, SUPERUSER_ID, [tick.x_cron_id.id], context)
        return super(crm_support_tickets, self).unlink(cr, uid, ids, context=context)

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        res = super(crm_support_tickets, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu)
        if view_type != 'form':
            return res
        users_obj = self.pool.get('res.users')
        all_uids = users_obj.search(cr,uid,[])
        non_portal_users = [npid for npid in all_uids if not users_obj.has_group(cr, npid, 'portal.group_portal')]
        doc = etree.XML(res['arch'])
        for node in doc.xpath("//field[@name='user_id']"):
            if non_portal_users:
                user_filter =  "[('id', 'in', " + str(tuple(non_portal_users)) + " )]"
                node.set('domain',user_filter)
        for node in doc.xpath("//field[@name='x_escalate_to']"):
            if non_portal_users:
                user_filter =  "[('id', 'in', " + str(tuple(non_portal_users)) + " )]"
                node.set('domain',user_filter)
        res['arch'] = etree.tostring(doc)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        pri_id = vals.get('priority',False)
#         faq_obj = self.pool.get('crm.support.faq')
        stage_id = vals.get('stage_id',False)
        if vals.get('partner_id'):
            vals['message_follower_ids'] = [(4, vals.get('partner_id'))]
        for tick in self.browse(cr, uid, ids, context=None):
            if pri_id:
                priority = self.pool.get('crm.ticket.priority').browse(cr, uid, pri_id, context=None)
                svals = {
                         'name': "Send E-mail alert to user for Ticket: " + str(tick.x_tick_id),
                         'interval_number': priority.interval_number or 0,
                         'interval_type': priority.interval_type or 'days',
                         'numbercall': priority.numberemail or 0,
                         'model':'crm.claim',
                         'priority':1,
                         'active':True,'doall':False,
                         'function':'_run_alertmail',
                         'args':'('+str(tick.id)+',)',
                         'user_id':uid
                         }
                if tick.x_cron_id:
                    self.pool.get('ir.cron').write(cr,SUPERUSER_ID,[tick.x_cron_id.id],svals,context=None)
                else:
                    x_cron_id = self.pool.get('ir.cron').create(cr,SUPERUSER_ID,svals,context=None)
#                     super(crm_support_tickets, self).write(cr, uid, ids, {'x_cron_id':x_cron_id,}, context)
                    vals.update({'x_cron_id':x_cron_id})
            if stage_id:
                tick_state = self.pool.get('crm.claim.stage').browse(cr,uid,stage_id).state
                if tick_state == 'done':
                    resol = tick.resolution
                    if not resol:
                        raise osv.except_osv(_('Information!'),_('You cannot settle the ticket without providing Resolution.'))
                    tick_id = tick.id
                    cr.execute("select count(*) from work_log_lines where ticket_log_id=%s",(tick_id,))
                    work_log_count = cr.fetchone()[0]
                    if work_log_count == 0:
                        raise osv.except_osv(_('Information!'),_('Please enter your work log first before closing the ticket.'))
                    else:                        
                        cr.execute("select time_spend from work_log_lines where ticket_log_id=%s order by write_date desc", (tick_id,))
                        latest_time_spend = cr.fetchone()[0]
                        print "pending count", latest_time_spend
                        if latest_time_spend =='0:00:00':
                            raise osv.except_osv(_('Information!'),_('Please select Stop Working first and enter the Actions taken before closing this ticket'))
                    self.send_response_email(cr, uid, [tick.id], context)
                    today = fields.datetime.now()
                    vals.update({'date_closed':today})
                else:
                    vals.update({'date_closed':False})
        upd = super(crm_support_tickets, self).write(cr, uid, ids, vals, context)
        return upd

    def get_signup_url(self, cr, uid, ids, context=None):
        assert len(ids) == 1
        document = self.browse(cr, uid, ids[0], context=context)
        partner = document.partner_id
        action = 'portal_claim.crm_case_categ_claim0'
        if not partner:
            partner = document.x_customer
        if not partner:
            return False
        partner.signup_prepare()
        
        return partner._get_signup_url_for_action(action=action, view_type='form', res_id=document.id)[partner.id]

    def btn_faq(self, cr, uid, ids, context=None):
        faq_obj = self.pool.get('crm.support.faq')
        for tick in self.browse(cr, uid, ids, context=None):
            
            fvals={'faq_title':tick.name or '',
                       'description':tick.description or '',
                       'categ_id':tick.categ_id.id or False,
                       'owner_tick':tick.id or False,
                       'resolution':tick.resolution,
                       'type_action':tick.type_action,
                   }
            fid = faq_obj.create(cr, uid, fvals,context)
            super(crm_support_tickets, self).write(cr, uid, tick.id, {'x_faq_id':fid,}, context)
        return True

    def send_ack_email(self, cr, uid, ids, context=None):
        email_template_obj = self.pool.get('email.template')
        context = context is not None and context or {}

        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'crm_support_tickets', 'email_template_support_acknowledge_mail')[1]
        except ValueError:
            template_id = False

        ctx = dict(context)
        ctx.update({
            'default_model': 'crm.claim',
            'default_res_id': ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_ticket_as_acknowledged': True
        })
        if template_id:
            for ticket in self.browse(cr, uid, ids, context=None):
                if ticket.email_from:
                    values = email_template_obj.generate_email(cr, uid, template_id, ticket.id, context=context)
     #               print "values::  ", values 
                    values['subject'] = "Support Ticket - " + str(ticket.x_tick_id)
                    values['email_to'] = ticket.email_from
                    values['email_from'] = ticket.company_id.email or ''
           #         values['email_cc'] = your_cc_address
#                    values['body_html'] = body_html_part
#                    values['body'] = body_html_part

                    mail_mail_obj = self.pool.get('mail.mail')
                    msg_id = mail_mail_obj.create(cr, uid, values, context=context)
                    if msg_id:
                        mail_mail_obj.send(cr, uid, [msg_id], context=ctx)
   #                     self.write(cr, uid, ids, {'acknowledged':True,},context=None)
        return True

    def send_response_email(self, cr, uid, ids, context=None):
        email_template_obj = self.pool.get('email.template')
        context = context is not None and context or {}
        ir_model_data = self.pool.get('ir.model.data')
        ir_attachment_obj=self.pool.get('ir.attachment')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'crm_support_tickets', 'email_template_support_closed_mail')[1]
        except ValueError:
            template_id = False

        ctx = dict(context)
        ctx.update({
            'default_model': 'crm.claim',
            'default_res_id': ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
        })
        if template_id:
            for ticket in self.browse(cr, uid, ids, context=None):
                if ticket.email_from:
                    values = email_template_obj.generate_email(cr, uid, template_id, ticket.id, context=context)
#                    print "values:: \n\n\n ", values 
                    values['subject'] = "Follow up on - " + str(ticket.x_tick_id)
                    values['email_to'] = ticket.email_from
                    values['email_from'] = ticket.company_id.email or ''
                    if ticket.x_ref_faq:
                        attachment_ids=ir_attachment_obj.search(cr,uid,[('res_id', '=', ticket.x_ref_faq.id)])
                        values['attachment_ids'] =[(6,0,attachment_ids)]
           #         values['email_cc'] = your_cc_address
#                    values['body_html'] = body_html_part
#                    values['body'] = body_html_part

                    mail_mail_obj = self.pool.get('mail.mail')
                    msg_id = mail_mail_obj.create(cr, uid, values, context=context)
                    if msg_id:
                        mail_mail_obj.send(cr, uid, [msg_id], context=ctx)

        return True

    def stop_work(self, cr, uid, ids,data, context=None):
        ##need to add the log details
        obj_wrklog=self.pool.get('work.log.lines')
        ids_log=obj_wrklog.search(cr,uid,[('ticket_log_id','=',ids[0])])
	print "ids log",ids_log
        stop_user=uid
	print "stop user",stop_user
        note=data.note or ''	   
	print "note",note
        obj_wrklog.write(cr,uid,[ids_log[0]],{'ticket_log_id':ids[0],'note':note, 'stop_user':stop_user})       
        return self.write(cr, uid, ids, {'is_working':False} ,context=context)

    def start_work(self, cr, uid, ids, context=None):
        #need to add the start time to the child table
        obj_wrklog=self.pool.get('work.log.lines')
        startuser=uid
        log_id=obj_wrklog.create(cr,uid,{'ticket_log_id':ids[0], 'start_user':startuser})
        # log_id=obj_wrklog.create(cr,uid,{'ticket_log_id':ids[0]})
        context['log_id'] = log_id
        return self.write(cr, uid, ids, {'is_working':True} ,context=context)

    def btn_ack(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        cust_email =False
        ackd = False
        for tick in self.browse(cr,uid, ids, context):
            cust_email = tick.email_from or False
#            ackd = tick.x_acknowledged
            partner = tick.partner_id
        if not cust_email:
            raise osv.except_osv(_('Information!'),_('Please define customer/contact person and a valid E-mail id to send Email!'))
        if ackd:
            raise osv.except_osv(_('Information!'),_('The acknowledge email is already sent to the customer!'))
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'crm_support_tickets', 'email_template_support_acknowledge_mail')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False 
        ctx = dict(context)
        ctx.update({
            'default_model': 'crm.claim',
            'default_res_id': ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_ticket_as_acknowledged': True
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }



    def onchange_partner_id(self, cr, uid, ids, cust, contact, email=False):
        
        if not contact:
            if cust:
                address = self.pool.get('res.partner').browse(cr, uid, cust)
                if address.cust_status:
                    warning = {
                           'title': _('Customer Status!'),
                           'message' : _(address.cust_status)
                           }
                    return {'warning': warning,'value': {'partner_id':False,'email_from': address.email, 'partner_phone': address.phone}}
                return {'value': {'partner_id':False,'email_from': address.email, 'partner_phone': address.phone}}
            else:
                return {'value': {
                              'email_from': False,
                              'partner_phone': False,
                              'x_customer':False
                            }
                        }
        address = self.pool.get('res.partner').browse(cr, uid, contact)
        cust_id =False
        if address.parent_id:
            cust_id = address.parent_id.id
        else:
            cust_id=contact
        if address.cust_status:
            warning = {
                   'title': _('Customer Status!'),
                   'message' : _(address.cust_status)
                 }
            return {'warning': warning, 'value': {'x_customer':cust_id,'email_from': address.email, 'partner_phone': address.phone}}
        return {'value': {'x_customer':cust_id,'email_from': address.email, 'partner_phone': address.phone}}


    def send_alert_email(self, cr, uid, ids, context=None):
        email_template_obj = self.pool.get('email.template')
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'crm_support_tickets', 'email_template_support_ticket_alert_mail')[1]
        except ValueError:
            template_id = False
        if template_id:
            
            def send_it(cr, uid, ticket, template_id, def_user_mails, context=None):
                values = email_template_obj.generate_email(cr, uid, template_id, ticket.id, context=context)
                values['subject'] = "Support Ticket - " + str(ticket.x_tick_id) + ", with Priority - "+ticket.priority.name+" is still pending."
                values['email_to'] = def_user_mails #ticket.user_id.email
                values['email_from'] = ticket.company_id.email or ''
                mail_mail_obj = self.pool.get('mail.mail')
                msg_id = mail_mail_obj.create(cr, uid, values, context=context)
                if msg_id:
                    mail_mail_obj.send(cr, uid, [msg_id], context=context)
                return True
                    
            for ticket in self.browse(cr, uid, ids, context=None):
                def_user_mails=False
                
                tick_comp = ticket.company_id.id
                if ticket.user_id.email:
                    def_user_mails = ticket.user_id.email
                    send_it(cr, uid, ticket, template_id, def_user_mails, context)
                else:
                    if tick_comp:
                        def_users_id =False
                        def_mgrs=False
                        def_uobj=self.pool.get('crm.ticket.mgr')
                        def_users_id = def_uobj.search(cr, uid, [('company_id', '=', tick_comp)])
                        if def_users_id:
                            def_mgrs = def_uobj.browse(cr,uid,def_users_id[0]).default_mgrs
                            if len(def_mgrs)>0:
                                def_user_mails = ''
                                for du in def_mgrs:
                                    def_user_mails = def_user_mails + (du.email and (du.email + ",") or '')
                        if def_user_mails:
                            send_it(cr, uid, ticket, template_id, def_user_mails, context)
                    
        return True

    def _run_alertmail(self, cr, uid, x_tick_id=False, use_new_cursor=False, context=None):
        #claim_obj = self.pool.get('crm.claim')
        if x_tick_id:
            cl_ids = self.search(cr,uid,[('state','in',['draft','open','pending']),('id','=',x_tick_id)])

            if len(cl_ids)>0:
                self.send_alert_email(cr, uid, cl_ids,context)

        return True

    def on_change_opportunity(self, cr, uid, ids, opportunity_id, context=None):
        values = {}
        if opportunity_id:
            opportunity = self.pool.get('crm.lead').browse(cr, uid, opportunity_id, context=context)
            values = {
                'section_id' : opportunity.section_id and opportunity.section_id.id or False,
                'partner_phone' : opportunity.phone,
#                 'partner_mobile' : opportunity.mobile,
                'partner_id' : opportunity.partner_id and opportunity.partner_id.id or False,
            }
        return {'value' : values}

    def on_change_ref_faq(self, cr, uid, ids, ref_faq, context=None):
        values = {}
        if ref_faq:
            faq = self.pool.get('crm.support.faq').browse(cr, uid, ref_faq, context=context)
            values = {
                'type_action' : faq.type_action or False,
                'resolution' : faq.resolution or False,
                }
        return {'value' : values}

    """def _res_portal(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for tick in self.browse(cursor, user, ids, context=context):
            res[tick.id] = tick.resolution
        return res"""


    def convert_opportunity(self, cr, uid, ids, opportunity_summary=False, partner_id=False, planned_revenue=0.0, probability=0.0, context=None):
        partner = self.pool.get('res.partner')
        opportunity = self.pool.get('crm.lead')
        opportunity_dict = {}
        default_contact = False
        for ticket in self.browse(cr, uid, ids, context=context):
            if not partner_id:
                partner_id = ticket.partner_id and ticket.partner_id.id or False
            if partner_id:
                address_id = partner.address_get(cr, uid, [partner_id])['default']
                if address_id:
                    default_contact = partner.browse(cr, uid, address_id, context=context)
            opportunity_id = opportunity.create(cr, uid, {
                            'name': opportunity_summary or ticket.name,
                            'planned_revenue': planned_revenue,
                            'probability': probability,
                            'partner_id': partner_id or False,
                            'mobile': default_contact and default_contact.mobile,
                            'section_id': ticket.section_id and ticket.section_id.id or False,
                            'description': ticket.description or False,
                            'priority': crm.AVAILABLE_PRIORITIES[2][0],
                            'type': 'opportunity',
                            'phone': ticket.partner_phone or False,
                            'email_from': default_contact and default_contact.email,
                        })
            vals = {
                    'partner_id': partner_id,
                    'x_opportunity_id' : opportunity_id,
            }
            self.write(cr, uid, [ticket.id], vals)
#            self.case_close(cr, uid, [ticket.id])
#            opportunity.case_open(cr, uid, [opportunity_id])
            opportunity_dict[ticket.id] = opportunity_id
        return opportunity_dict


    def action_button_convert2opportunity(self, cr, uid, ids, context=None):
        """
        Convert a support ticket into an opp and then redirect to the opp view.

        :param list ids: list of tickets ids to convert (typically contains a single id)
        :return dict: containing view information
        """
        if len(ids) != 1:
            raise osv.except_osv(_('Warning!'),_('It\'s only possible to convert one support ticket at a time.'))

        opportunity_dict = self.convert_opportunity(cr, uid, ids, context=context)
        return self.pool.get('crm.lead').redirect_opportunity_view(cr, uid, opportunity_dict[ids[0]], context)

    # -------------------------------------------------------
    # Mail gateway
    # -------------------------------------------------------

    def message_new(self, cr, uid, msg, custom_values=None, context=None):
        """ Overrides mail_thread message_new that is called by the mailgateway
            through message_process.
            This override updates the document according to the email.
        """
        if custom_values is None: custom_values = {}
        fetchmail_server_id = context.get('fetchmail_server_id', False)
        comp = False
        parent = False
        contact_id = msg.get('author_id', False)
        if contact_id:
            parent = self.pool.get('res.partner').browse(cr, uid, contact_id).parent_id
        if fetchmail_server_id:
            comp = self.pool.get('fetchmail.server').browse(cr,uid,fetchmail_server_id).company_id.id
        defaults = {
            'company_id': comp,
            'partner_id':parent and contact_id or False,
            'x_customer':parent and parent.id or contact_id
        }
        defaults.update(custom_values)
        return super(crm_support_tickets,self).message_new(cr, uid, msg, custom_values=defaults, context=context)






crm_support_tickets()


class work_log_lines(osv.osv):
    _name = "work.log.lines"
    _description = "Support work Log Time"
    _order = "create_date desc"

    def _time_spend(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            cdate= datetime.strptime(line.create_date, '%Y-%m-%d %H:%M:%S')
            wdate= datetime.strptime(line.write_date, '%Y-%m-%d %H:%M:%S')
            diff = wdate - cdate
            res[line.id] =diff
        return res


    _columns = {
        'ticket_log_id' : fields.many2one('crm.claim', 'Ticket Reference',  ondelete='cascade'),
        'note':fields.text('Actions Taken'),
        'create_date': fields.datetime('Start Time', readonly=True),
        'write_date' : fields.datetime('End Time',readonly=True),
        'time_spend' : fields.function(_time_spend, string='Duration',type="char",store=True),
        'start_user' :fields.many2one('res.users','Start User'),
        'stop_user' :fields.many2one('res.users','Stop User'),
    }

    _defaults = {
        'note' : 'Pending'
    }


#===============================================================================
# #     Adding company field in incoming mail server
#===============================================================================


class fetchmail_server(osv.osv):
    """Incoming POP/IMAP mail server account"""
    _inherit = 'fetchmail.server'
    _columns = {
                'company_id': fields.many2one('res.company', 'Company'),
                }
    _defaults={
               'company_id': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'fetchmail.server', context=c),
               }
fetchmail_server()



