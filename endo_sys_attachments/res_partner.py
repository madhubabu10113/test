# -*- coding: utf-8 -*-
##############################################################################
#
# Endosoft
#
##############################################################################

from openerp.osv import osv, fields
from collections import Counter
from openerp.tools.translate import _
from datetime import date, datetime, timedelta
import time


	
class document_file(osv.osv):
 	#_inherit = 'ir.attachment'
	_inherit = 'room.lines'  

	_columns = {
	#'attachment': fields.many2many('ir.attachment','room_lines_rel','room_id', 'attachment_id','Attachments'),
	'attachment': fields.many2many('endo.attachments', 'room_lines_rel','room_id', 'attachment_id', 'Attachments'),

}

document_file()


class licensce_lines(osv.osv):
	_inherit = 'licensce.lines'
	_columns = {
	'x_current_date':fields.datetime('Current Date'),
}
	_defaults={
			'x_current_date': lambda *a: time.strftime('%Y-%m-%d'),
			}
licensce_lines()


