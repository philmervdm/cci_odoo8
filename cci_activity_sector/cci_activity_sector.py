# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2008 CCI Connect ASBL. (http://www.cciconnect.be) All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################
from openerp import models, fields, api , _
from openerp.exceptions import Warning

class res_partner_activsector(models.Model):
    
    @api.constrains('parent_id')
    def _check_recursion(self):
        level = 100
        ids = self.ids
        while len(ids):
            self.env.cr.execute('select distinct parent_id from res_partner_activsector where id in %s', (tuple(ids),))
            ids = filter(None, map(lambda x:x[0], self.env.cr.fetchall()))
            if not level:
                raise Warning(_('Error ! You can not create recursive sectors.'))
            level -= 1
        return True

    _description='Partner CCI Activity Sector'
    _name = 'res.partner.activsector'
    
    code = fields.Char('Sector Code', required=True, size=6)
    name = fields.Char('Sector Name', required=True, size=64, translate=True)
    parent_id = fields.Many2one('res.partner.activsector', 'Parent Sector', select=True)
    child_ids = fields.One2many('res.partner.activsector', 'parent_id', 'Child Sectors')
    active = fields.Boolean('Active', default=True, help="The active field allows you to hide the sector without removing it.")
    directly = fields.Boolean('Directly usable', help='The concerned sector can be directly used by a partner, it isn\'t a header sector')
    
    _order = 'code'

class res_partner_address(models.Model):
    _inherit = "res.partner"
    _description = "res.partner"

    sector1 = fields.Many2one('res.partner.activsector','Sector 1')
    sector2 = fields.Many2one('res.partner.activsector','Sector 2')
    sector3 = fields.Many2one('res.partner.activsector','Sector 3')
