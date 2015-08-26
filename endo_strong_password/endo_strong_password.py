# -*- coding: utf-8 -*-
##############################################################################
#
# Endosoft
#
##############################################################################

from openerp.osv import fields,osv
from openerp.tools.translate import _

#from datetime import datetime,date
#from dateutil.relativedelta import relativedelta


class res_user(osv.osv):
    _inherit = 'res.users'
    
    def change_password(self, cr, uid, old_passwd, new_passwd, context=None):
        self.check(cr.dbname, uid, old_passwd)
        if new_passwd:
            import re
            mobj = re.match(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).{6,20}', new_passwd)
            if mobj == None:
                raise osv.except_osv(_('Warning!'),_('Your password was not changed!'\
                                                     'Please use a password with at least 6 characters'\
                                                     'containing at least one numeric digit, one UPPERCASE,'\
                                                     'one lowercase letter and one Symbol character.'))
            else:
                return self.write(cr, uid, uid, {'password': new_passwd})
        raise osv.except_osv(_('Warning!'), _("Setting empty passwords is not allowed for security reasons!"))

    
res_user()

class change_password_user(osv.TransientModel):
    _inherit = 'change.password.user'
    _description = 'Change Password Wizard User'
    
    def change_password_button(self, cr, uid, ids, context=None):
        for user in self.browse(cr, uid, ids, context=context):
            pwd = user.new_passwd
            import re
            mobj = re.match(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).{6,20}', pwd)
            if mobj == None:
                raise osv.except_osv(_('Warning!'),_('Your password was not changed!'\
                                                     'Please use a password with at least 6 characters'\
                                                     'containing at least one numeric digit, one UPPERCASE,'\
                                                     'one lowercase letter and one Symbol character.'))
            else:
                self.pool.get('res.users').write(cr, uid, user.user_id.id, {'password': pwd})
