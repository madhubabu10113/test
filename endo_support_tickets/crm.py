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

class crm_case_categ(osv.osv):
    _inherit = "crm.case.categ"
    _order = 'name'
crm_case_categ()


