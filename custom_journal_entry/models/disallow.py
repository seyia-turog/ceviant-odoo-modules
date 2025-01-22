from odoo import models, fields, api
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        move = super(AccountMove, self).create(vals)
        move._check_liquidity_account_balance()
        return move

    def write(self, vals):
        res = super(AccountMove, self).write(vals)
        self._check_liquidity_account_balance()
        return res

    def _check_liquidity_account_balance(self):
        for line in self.line_ids:
            if line.account_id.account_type == 'asset_cash':
                balance = sum(
                    (move_line.debit - move_line.credit) for move_line in self.env['account.move.line'].search([('account_id', '=', line.account_id.id)])
                )
                if balance < 0:
                    raise UserError(
                        "Insufficient funds in the liquidity account: %s. Balance cannot be negative!" % line.account_id.name
                    )
