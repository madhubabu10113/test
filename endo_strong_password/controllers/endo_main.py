# -*- coding: utf-8 -*-

import openerp.addons.web.controllers.main as main

import openerp
import openerp.modules.registry
from openerp.tools.translate import _
from openerp.tools import config
import operator
#----------------------------------------------------------
# OpenERP Web helpers
#----------------------------------------------------------
class endo_Session(main.Session):
    _cp_path = "/web/session"

    @openerpweb.jsonrequest
    def change_password (self,req,fields):
        old_password, new_password,confirm_password = operator.itemgetter('old_pwd', 'new_password','confirm_pwd')(
                dict(map(operator.itemgetter('name', 'value'), fields)))
        if not (old_password.strip() and new_password.strip() and confirm_password.strip()):
            return {'error':_('You cannot leave any password empty.'),'title': _('Change Password')}
        if new_password != confirm_password:
            return {'error': _('The new password and its confirmation must be identical.'),'title': _('Change Password')}
        try:
            if req.session.model('res.users').change_password(
                old_password, new_password):
                return {'new_password':new_password}
        except Exception:
            return {'error': _('The old password you provided is incorrect or provide strong password, your password was not changed.'), 'title': _('Change Password')}
        return {'error': _('Error, password not changed !'), 'title': _('Change Password')}


# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
