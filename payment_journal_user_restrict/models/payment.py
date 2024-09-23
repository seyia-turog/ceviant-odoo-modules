

from odoo import api, fields, models, Command, _
import json
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


from collections import defaultdict, namedtuple





class ResUsers(models.Model):
    _inherit = 'res.users'

    journal_ids = fields.Many2many(string='Allwed Journals', comodel_name="account.journal", relation="journal_id_rel",column1="user_id" , column2="journal_id")
    account_journal_comp_ids = fields.Many2many('account.journal',compute='_compute_journal_ids',string='Allowed Journals For Current Company')

    def _compute_journal_ids(self):
        if self.journal_ids:
            self.account_journal_comp_ids = self.journal_ids.filtered(lambda m: m.company_id.id == self.env.company.id).ids
        else:
            self.account_journal_comp_ids = False


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    def _default_domain_user_ids(self):
        return [('groups_id', 'in', self.env.ref('account.group_account_user').id)]


    user_ids = fields.Many2many(
        comodel_name="res.users",
        string="Allowed Users",
        relation="journal_id_rel",column1="journal_id",column2="user_id",domain=lambda self: self._default_domain_user_ids())




class AccountPayment(models.Model):
    _inherit = 'account.payment'


    allowed_users = fields.Many2many("res.users",string='Allowed Users',compute='_allowed_users')
    receive_payment_invisable = fields.Boolean(compute='_allowed_users',string="Receive Payment Invisable")

    # state = fields.Selection(selection_add=[('first_confirm', 'Send to Confirm')], ondelete={'draft': 'set default'})


    @api.depends('is_internal_transfer','journal_id','destination_journal_id')
    def _allowed_users(self):
        for record in self:
            user = self.env.user
            record.receive_payment_invisable = False
            record.allowed_users = False
            if record.is_internal_transfer and (record.destination_journal_id and record.destination_journal_id.user_ids):
                record.allowed_users = record.destination_journal_id.user_ids
                if record.allowed_users and (user not in record.destination_journal_id.user_ids):
                    record.receive_payment_invisable = True
                else:
                    record.allowed_users = False

            else:
                if record.journal_id and record.journal_id.user_ids:
                    record.allowed_users = record.journal_id.user_ids
                    record.update({'receive_payment_invisable': False})
                else:
                    record.allowed_users = False
                    record.update({'receive_payment_invisable': False})




class AccountMove(models.Model):
    _inherit = 'account.move'

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
