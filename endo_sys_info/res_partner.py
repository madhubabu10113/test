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
#from datetime import datetime,date
#from dateutil.relativedelta import relativedelta

class res_partner(osv.osv):
    _inherit = 'res.partner'

    def button_function(self, cr, uid, ids, context=None):
        print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
        return True

    def onchange_address(self, cr, uid, ids, use_parent_address, 
parent_id, context=None):
        result = super(res_partner,self).onchange_address(cr, uid, ids, use_parent_address, parent_id, context=context)
        if parent_id:
            parent = self.browse(cr, uid, parent_id, context=context)
            #print "#################",parent.system_installed,[x.id for x in o.booking_line]
#            result['value'] = {'system_installed':parent.system_installed.id or '',
#                            'db_server': parent.db_server.id or '',
#                            'his' : parent.his.id or '',
#                            'pacs' : parent.pacs.id or '',
#                            'sitelic': parent.sitelic,
#                            'supdate' : parent.supdate or '',
#                            }
            result['value'] = {'system_installed':[x.id for x in parent.system_installed] or [],
                            'db_server': parent.db_server.id or '',
                            'his' : [x.id for x in parent.his] or [],
                            'pacs' : parent.pacs.id or '',
                            'sitelic': parent.sitelic,
                            'supdate' : parent.supdate or '',
                           # 'x_department_parent':parent_id or '',
                            }


        return result

    def onchange_type(self, cr, uid, ids, is_company, context=None):
        result = super(res_partner,self).onchange_type(cr, uid, ids, is_company, context=context)
        if is_company:
            result['value'] = {
                            'x_location':False,
                            #'x_isdept':False,
                            'is_company':True,
                            }
        return result

    def onchange_type_location(self, cr, uid, ids, x_location,context=None):
        value = {}
        obj=self.browse(cr, uid, ids, context)
        domain = {'title': [('domain', '=', 'contact')]}
        if x_location:
            value= {'title':False, 'is_company':False, 
#                    'x_isdept':False,
                    'x_location':True}
        return {'value': value, 'domain': domain}

    def create(self, cr, uid, vals, context=None):
        if 'parent_id' in vals.keys() and 'use_parent_address' in vals.keys():
            onchangeResult = self.onchange_address(cr, uid, [],vals['use_parent_address'], vals['parent_id'], context=context)
            if onchangeResult.get('value') and onchangeResult['value'].get('system_installed'):
                sys_ids = onchangeResult['value']['system_installed']
                vals['system_installed'] = [(6,0,sys_ids)]

            if onchangeResult.get('value') and onchangeResult['value'].get('db_server'):
                vals['db_server'] = onchangeResult['value']['db_server']
            if onchangeResult.get('value') and onchangeResult['value'].get('his'):
                
                vals['his'] = [(6,0,onchangeResult['value']['his'])]
            if onchangeResult.get('value') and onchangeResult['value'].get('pacs'):
                vals['pacs'] = onchangeResult['value']['pacs']
            if onchangeResult.get('value') and onchangeResult['value'].get('sitelic'):
                vals['sitelic'] = onchangeResult['value']['sitelic']
            return super(res_partner, self).create(cr, uid, vals, context=context)
        else:
            return super(res_partner, self).create(cr, uid, vals, context=context)

    def write(self,cr, uid, ids,vals,context=None):
        res={}
        if 'is_company' in vals.keys():
            if not vals['is_company']:
                for parent in self.browse(cr, uid, ids, context=context):
                    if parent.child_ids:
                        raise osv.except_osv(_('Error'),
                            _('You cannot remove this from Company, as it contains Contacts for this company'))

        if 'parent_id' in vals.keys():
            if vals['parent_id']:
                parent_company=self.browse(cr,uid,vals['parent_id'])
                res = {
                    'system_installed':[(6,0,[x.id for x in parent_company.system_installed] or [])],
                    'db_server' : parent_company.db_server.id or '',
                    'his' : [(6,0,[x.id for x in parent_company.his] or [])],
                    'pacs' : parent_company.pacs.id or '',
                    'sitelic' : parent_company.sitelic or '',
                }
            else:
                res = {
                    'system_installed':[(6,0,[])],
                    'db_server' : '',
                    'his' : [(6,0,[])],
                    'pacs' : '',
                    'sitelic' : '',
                }
        vals.update(res)
        return super(res_partner, self).write(cr, uid, ids, vals, context=context)

    def test(self, cr, uid, ids, field_names=None, arg=None, context=None):
        result={}
        summery_obj=self.pool.get('summery.lines')
        for x in self.browse(cr, uid, ids):
            su=summery_obj.search(cr,uid, [('summery_id','=',ids[0])])
            c=summery_obj.unlink(cr, uid, su)
            for loca in x.location_lines:
                for room_data in loca.name.room_lines:
                    for license_data in room_data.licensce_lines:
                        summery_obj.create(cr, uid,{
                                'summery_id':ids[0],
                                'location_id':loca.name.id,
                                'room_id':room_data.name.id,
                                'licensce':license_data.name.id,
                                'comp_name':license_data.comp_name or 'Nill',
                                'exe_version':license_data.exe_version.id or False,
                                'installed_date':license_data.installed_date,
                                'support_end':license_data.support_end,
                                'deactive':license_data.deactive,
                                
                                'comments': license_data.comments
                                })
        return result



    _columns = {

        'x_location':fields.boolean('Is a Location'),
        'x_department': fields.char('Department',size=128),
        'x_location_name': fields.char('Location',size=128),
        'x_other_phone': fields.char('Other Phone', size=64),
        'x_work_phone': fields.char('Work Phone', size=64),
        'supdate' : fields.date('Support Date'),
        'sitelic' : fields.boolean('Site License'),
        'remote_conn': fields.char('Remote Connection Details',size=256),
        'db_server': fields.many2one('sys.info.db','Database server'),
        'pacs' : fields.many2one('sys.pacs','PACS'),
        'room_lines' : fields.one2many('room.lines','room_id','Rooms'),
        'summery_lines' : fields.one2many('summery.lines','summery_id','Summary',readonly=True),
        'summery_line': fields.function(test,type='one2many', relation='summery.lines',string='Summary'),
        'dicom_lines' : fields.one2many('dicom.lines','dicom_id','DICOM'),
        'location_lines': fields.one2many('location.line','part_loc_id','Locations'),
        'interfacs_lines': fields.one2many('interfaces.lines','inter_id','Interfaces'),
        'system_installed': fields.many2many('sys.installed','sys_info_partner_rel','x_system_id','x_partner_id','System Installed'),
        'his' : fields.many2many('sys.his','his_partner_rel','x_his_id','x_partner_id','Hospital Information System'),
        'additional_notes' : fields.text('Additional Notes'),
	}

    _defaults = {
        #'x_person': 1,
        'supdate': (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')
        
    }

#Summery Lines 
class summery_lines(osv.osv):
    _name = 'summery.lines'
    _columns = {
        'summery_id' : fields.many2one('res.partner','Summary',required=True,ondelete="cascade"),
        'location_id': fields.many2one('res.partner','Location'),
        'room_id':fields.many2one('sys.room','Room Name'),
        'licensce' : fields.many2one('product.product','License'),
        'comp_name': fields.char('Computer name', size=32),
        'exe_version':fields.many2one('sys.exe.version','Release #'),
        'installed_date': fields.date('Date of installation'),
        'support_end': fields.date('Support End Date'),
        'deactive': fields.boolean('Deactive'),
        'comments': fields.text('Comments')
        
    }

#Room Lines
class room_lines(osv.osv):
    _name = 'room.lines'
   
    def _get_details(self, cursor, user, ids, name, arg, context=None):
        res ={}
        for room in self.browse(cursor,user, ids, context=context):
            comment=''
            a=[]
            comment1 = "Licenses:(Name,Computer Name, Installed Date, Support EndDate)\n"
            for l in room.licensce_lines:
                print "License",l.name.name,l.comp_name,l.installed_date,l.support_end
                comment1 = "%s %s , %s , %s , %s\n"%(comment1,l.name.name,l.comp_name or "nill",l.installed_date,l.support_end)
            comment2 = "Video Processors:(Brand , Type)\n"
            for l in room.video_process_lines:
                print "Video Processors",l.name.name
                comment2 = "%s %s , %s\n"%(comment2,l.name.name or 'nill',l.type_id.name or 'nill')
            res[room.id] = comment1 + comment2
        return res

    def _get_room_name(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for record in self.browse(cursor, user, ids, context=context):
            res[record.id] = record.name.name
        return res
    
    _rec_name = 'room_name'
    
    _columns = {
        'room_id' : fields.many2one('res.partner','Location',required=True,ondelete="cascade"),
        'name' : fields.many2one('sys.room','Room Name',required=True),
#        'remote_conn_room': fields.char('Remote Connection Details',size=256),
        'room_name':fields.function(_get_room_name,type='char',string='Room'),
        'remote_conn_room': fields.text('Remote Connection Details'),
        'licensce_lines' : fields.one2many('licensce.lines','licenscee_id','Product Installed'),
        'cableing_lines': fields.one2many('room.cable.lines','cable_id','Cables'),
        'cust_cable_lines': fields.one2many('cust.cable.lines','cust_cabl_id','Custom Cable'),
        'video_process_lines' : fields.one2many('video.process.lines','video_pro_id','Video Processors'),
        'other_equp_lines' : fields.one2many('other.equp.lines','other_equp_id','Other Equipment'),
        'comment':fields.function(_get_details,string="Summary",type='text'),
        'notes': fields.text('Notes'),
        
#         'file_ids': fields.one2many('ir.attachment', 'res_id', 'Attachments', domain="[('res_model','=','realestate.property')]",),
        
    }

#Interfaces_lines
class interfaces_lines(osv.osv):
    _name = "interfaces.lines"
    _columns = {
        'inter_id': fields.many2one('res.partner','Interface',required=True,ondelete="cascade"),
        'name': fields.many2one('product.product','Interface',required=True),
        'his_id': fields.many2one('sys.his','HIS'),
        'listening_ip' : fields.char('Listening IP/Port #',size=32),
        'sending_ip' : fields.char('Sending IP/Port #',size=32),
        'comments': fields.text('Comments'),
    }


class dicom_lines(osv.osv):
    _name = "dicom.lines"
    _columns = {
        'dicom_id': fields.many2one('res.partner','DICOM',required=True,ondelete="cascade"),
        'name': fields.many2one('sys.dicom.type','Type',required=True),
        'node' : fields.char('Node',size=32),
        'port_no' : fields.char('Port #',size=32),
        'calling_ae': fields.char('Calling AE',size=32),
        'called_ae': fields.char('Called AE',size=32),
        'comments': fields.text('Comments'),
    }



#Location Lines
class location_line(osv.osv):
    _name = 'location.line'
    def view_location(self, cr, uid, ids, context=None):
        res_id=''
        for i in self.browse(cr, uid, ids,context=context):
            res_id=i.name.id or ids[0]
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'base', 'view_partner_form')
        view_id = view_ref and view_ref[1] or False,
        return {
            'type' : 'ir.actions.act_window',
            'name' : _('res.partner.form'),
            'res_model': 'res.partner',
            'res_id': res_id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'nodestroy': True,
        }

    _columns = {
        'part_loc_id': fields.many2one('res.partner', 'Location Reference', required=True, ondelete='cascade'),
        'name' : fields.many2one('res.partner', 'Location Reference',required=True,domain=[('x_location','=',True)]),
    }




class licensce_lines(osv.osv):
    _name = 'licensce.lines'

    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        res = []
        result = super(licensce_lines, self).name_get(cr, uid, ids, context)
        if context.get('frm_tick'):
            for record in result:
                obj = self.browse(cr,uid,record[0])
                name=obj.name.name + (obj.comp_name and (", " + obj.comp_name) or "") 
                res.append((obj.id, name))
            return res
        return result
    
    def _get_lic_name(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for record in self.browse(cursor, user, ids, context=context):
            res[record.id] = record.name.name
        return res
    
    #_rec_name = 'lic_name'
    _rec_name = 'name'

    _columns = {
        'licenscee_id' : fields.many2one('room.lines','Licenses', required=True, ondelete='cascade'),
        'name' : fields.many2one('product.product','Product Installed',required=True),
        #'lic_name' : fields.function(_get_lic_name,type='char',string='Liscence'),
        'comp_name': fields.char('Computer name', size=32),
        'exe_version':fields.many2one('sys.exe.version','Release #'),
        'installed_date': fields.date('Date of installation'),
        'support_start': fields.date('Support Start Date'),
        'support_end': fields.date('Support End Date'),
        'deactive': fields.boolean('Deactive'),
        'comments': fields.text('Comments'),

    }
    _defaults = {
        'installed_date' : fields.date.context_today,
        'support_start' : fields.date.context_today,
        'support_end': (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S'),
    }
class room_cable_lines(osv.osv):
    _name ='room.cable.lines'
    _columns = {
        'cable_id': fields.many2one('room.lines','Cables', required=True, ondelete='cascade'),
        'name' : fields.many2one('product.product','Cables',required=True),
        'comp_name': fields.char('Computer name', size=32),
        'serial_num' : fields.char('Serial Number', size=32),
        'installed_date': fields.date('Date of installation'),
        'cable_length': fields.char('Cable Length',size=32),
        'comments': fields.text('Comments'),
       
    }
class cust_cable_lines(osv.osv):
    _name = 'cust.cable.lines'
    _columns = {
        'cust_cabl_id': fields.many2one('room.lines','Custom Cable',required=True,ondelete='cascade'),
        'name':fields.many2one('sys.cable.type','Cable Type',required=True),
        'length': fields.many2one('sys.cable.length','Length'),
        'communication': fields.many2one('sys.cable.communication','Communication'),
        'comments': fields.text('Comments'),
        
    }
class video_process_lines(osv.osv):
    _name="video.process.lines"
    _columns = {
        'video_pro_id' :fields.many2one('room.lines','Video Processors', required=True, ondelete='cascade'),
        'name': fields.many2one('sys.video.process.brnd','Brand',required=True),
        'type_id': fields.many2one('sys.video.process.type','Type'),
        'comm_id' : fields.many2one('sys.video.process.com','Communication'),
        'comments': fields.text('Comments'),
    }
class other_equp_lines(osv.osv):
    _name="other.equp.lines"
    _columns = {
        'other_equp_id' :fields.many2one('room.lines','Other Equipments', required=True, ondelete='cascade'),
        'name': fields.many2one('sys.other.equ.brnd','Brand',required=True),
        'type_id': fields.many2one('sys.other.equ.type','Type'),
        'comm_id' : fields.many2one('sys.other.equ.com','Communication'),
        'comments': fields.text('Comments'),
    }

res_partner()
