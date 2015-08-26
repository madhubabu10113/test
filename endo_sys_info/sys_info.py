# -*- coding: utf-8 -*-
##############################################################################
#
# Endosoft
#
##############################################################################
from openerp.osv import fields,osv

# Creating some new objects for endosoft functionality
# System Installed

class sys_installed(osv.osv):
    _name = 'sys.installed'
    _description = 'System Installed'
    _columns = {
        'name' : fields.char('Name', size=32,required="1"),
        'description': fields.text('Description'),
    }

#System Information System Database
class sys_info_db(osv.osv):
    _name = 'sys.info.db'
    _description = 'System Information DB'
    _columns = {
        'name' : fields.char('Name', size=32,required="1"),
        'description': fields.text('Description'),
    }
#Hospital Information System

class sys_his(osv.osv):
    _name = 'sys.his'
    _description = 'Hospital Information System'
    _columns ={
        'name' : fields.char('Name',size=32,required="1"),
        'description': fields.text('Description'),
    }

#System PACS
class sys_pacs(osv.osv):
    _name = 'sys.pacs'
    _description = 'PACS'
    _columns ={
        'name' : fields.char('Name',size=32,required="1"),
        'description': fields.text('Description'),
    }

# System Rooms

class sys_room(osv.osv):
    _name = 'sys.room'
    _description ='Rooms'
    _columns = {
        'name' : fields.char('Name', size=32,required="1"),
#        'description': fields.text('Description'),
    }

#Custom Cabling

class sys_cable_type(osv.osv):
    _name = 'sys.cable.type'
    _description = 'Custom Cable Type'
    _columns = {
        'name':fields.char('Cable Type',required="1"),
    }
class sys_cable_length(osv.osv):
    _name = 'sys.cable.length'
    _description = 'Custom Cable Length'
    _columns = {
        'name':fields.char('Cable Length',required="1"),
    }
class sys_cable_communication(osv.osv):
    _name = 'sys.cable.communication'
    _description = 'Custom Communication'
    _columns = {
        'name':fields.char('Communication',required="1"),
    }

#Video Processors

class sys_video_process_brnd(osv.osv):
    _name = 'sys.video.process.brnd'
    _description = 'System Video Processors Brand'
    _columns = {
        'name': fields.char('Name',size=32,required="1"),
    }

class sys_video_process_type(osv.osv):
    _name = 'sys.video.process.type'
    _description = 'System Video Processors Type'
    _columns = {
        'name': fields.char('Name',size=32,required="1"),
    }
class sys_video_process_com(osv.osv):
    _name = 'sys.video.process.com'
    _description = 'System Video Processors Com'
    _columns = {
        'name': fields.char('Name',size=32,required="1"),
    }


#Other Equipment

class sys_other_equ_brnd(osv.osv):
    _name = 'sys.other.equ.brnd'
    _description = 'System Other Equipment Brand'
    _columns = {
        'name': fields.char('Name',size=32,required="1"),
    }

class sys_other_equ_type(osv.osv):
    _name = 'sys.other.equ.type'
    _description = 'System Other Equipment Type'
    _columns = {
        'name': fields.char('Name',size=32,required="1"),
    }
class sys_other_equ_com(osv.osv):
    _name = 'sys.other.equ.com'
    _description = 'System Other Equipment Com'
    _columns = {
        'name': fields.char('Name',size=32,required="1"),
    }
class sys_dicom_type(osv.osv):
    _name = 'sys.dicom.type'
    _description = 'DICOM Type'
    _columns = {
        'name' : fields.char('Name',size=32,required="1"),
    }
class sys_exe_version(osv.osv):
    _name = 'sys.exe.version'
    _description = 'EXE Version'
    _columns = {
        'name' : fields.char('Name',size=32,required="1"),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
