#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero
import logging

_logger =logging.getLogger(__name__)

class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'

    currency_id = fields.Many2one('res.currency', string='Currency', related='contract_id.currency_id',readonly=True,store=True)


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    #input_line_ids = fields.One2many('hr.payslip.input', 'payslip_id', string='Payslip Inputs', readonly=True,
    #                                 states={'draft': [('readonly', False)]}, copy=True)
    input_line_ids = fields.One2many('hr.payslip.input', 'payslip_id', string='Payslip Inputs', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', related='contract_id.currency_id',readonly=True,store=True)

    @api.model
    def is_readonly(self, record):
        return record.state != 'draft'



    def action_payslip_done(self):
        """
        Override action_payslip_done without calling the super.
        Code of the super already in two lines:
           slip.compute_sheet()
           slip.write({'move_id': move.id, 'date': date,'state': 'done'})
        :return:
        """
        precision = self.env['decimal.precision'].precision_get('Payroll')
        for slip in self:
            # slip.compute_sheet()
            slip.action_compute_sheet()
            line_ids = []
            debit_sum = 0.0
            credit_sum = 0.0
            date = slip.date or slip.date_to
            company_currency = slip.company_id.currency_id
            slip_currency = slip.currency_id
            name = _('Payslip of %s') % (slip.employee_id.name)
            move_dict = {
                'narration': name,
                'ref': slip.number,
                'journal_id': slip.journal_id.id,
                'date': date,
            }
            # if not any(line.salary_rule_id.account_debit_id and line.salary_rule_id.account_credit_id for line in
            #            slip.details_by_salary_rule_category_ids):
            #     raise UserError(_('Missing Debit Or Credit Account in Salary Rule'))
            for line in slip.details_by_salary_rule_category_ids:
                amount = slip_currency.round(slip.credit_note and -line.total or line.total)
                if slip_currency.is_zero(amount):
                    continue
                amount_currency = False
                if slip_currency != company_currency:
                    amount_currency = amount
                    #amount = slip_currency.with_context(date=date).compute(amount, company_currency)
                    amount = slip_currency._convert(amount, company_currency, self.env.user.company_id,
                                                           date)

                debit_account_id = line.salary_rule_id.account_debit_id.id
                credit_account_id = line.salary_rule_id.account_credit_id.id

                if debit_account_id:
                    debit_line = (0, 0, {
                        'name': line.name,
                        'partner_id': line._get_partner_id(credit_account=False),
                        'account_id': debit_account_id,
                        'journal_id': slip.journal_id.id,
                        'date': date,
                        'amount_currency': company_currency != slip_currency and amount_currency or amount,
                        'currency_id': company_currency != slip_currency and slip_currency.id or slip_currency.id,
                        'debit': amount > 0.0 and amount or 0.0,
                        'credit': amount < 0.0 and -amount or 0.0,
                        #'analytic_distribution': line.salary_rule_id.analytic_distribution,
                        'tax_line_id': line.salary_rule_id.account_tax_id.id,
                    })
                    line_ids.append(debit_line)
                    debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']

                if credit_account_id:
                    credit_line = (0, 0, {
                        'name': line.name,
                        'partner_id': line._get_partner_id(credit_account=True),
                        'account_id': credit_account_id,
                        'journal_id': slip.journal_id.id,
                        'date': date,
                        'amount_currency': company_currency != slip_currency and -amount_currency or -amount,
                        'currency_id': company_currency != slip_currency and slip_currency.id or slip_currency.id,
                        'debit': amount < 0.0 and -amount or 0.0,
                        'credit': amount > 0.0 and amount or 0.0,
                        #'analytic_distribution': line.salary_rule_id.analytic_distribution,
                        'tax_line_id': line.salary_rule_id.account_tax_id.id,
                    })
                    line_ids.append(credit_line)
                    credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

            #if float_compare(credit_sum, debit_sum, precision_digits=precision) == -1:
            if slip_currency.compare_amounts(credit_sum, debit_sum) == -1:
                acc_id = slip.journal_id.default_account_id.id
                if not acc_id:
                    raise UserError(_('The Expense Journal "%s" has not properly configured the Credit Account!') % (slip.journal_id.name))
                amount_currency = False
                amount = debit_sum - credit_sum
                if slip_currency != company_currency:
                    #amount_currency = -company_currency.with_context(date=date).compute(amount, slip_currency)
                    amount_currency = -company_currency._convert(amount, slip_currency, self.env.user.company_id,
                                                           date)
                adjust_credit = (0, 0, {
                    'name': _('Adjustment Entry'),
                    'partner_id': False,
                    'account_id': acc_id,
                    'amount_currency': company_currency != slip_currency and amount_currency or amount,
                    'currency_id': company_currency != slip_currency and slip_currency.id or slip_currency.id,
                    'journal_id': slip.journal_id.id,
                    'date': date,
                    'debit': 0.0,
                    'credit': amount,
                })
                line_ids.append(adjust_credit)

            #elif float_compare(debit_sum, credit_sum, precision_digits=precision) == -1:
            elif slip_currency.compare_amounts(debit_sum, credit_sum) == -1:
                acc_id = slip.journal_id.default_account_id.id
                if not acc_id:
                    raise UserError(_('The Expense Journal "%s" has not properly configured the Debit Account!') % (slip.journal_id.name))
                amount_currency = False
                amount  = credit_sum - debit_sum
                if slip_currency != company_currency:
                    #amount_currency = company_currency.with_context(date=date).compute(amount,slip_currency)
                    amount_currency = company_currency._convert(amount, slip_currency, self.env.user.company_id,
                                                           date)
                adjust_debit = (0, 0, {
                    'name': _('Adjustment Entry'),
                    'partner_id': False,
                    'account_id': acc_id,
                    'journal_id': slip.journal_id.id,
                    'amount_currency': company_currency != slip_currency and amount_currency or amount,
                    'currency_id': company_currency != slip_currency and slip_currency.id or slip_currency.id,
                    'date': date,
                    'debit': amount,
                    'credit': 0.0,
                })
                line_ids.append(adjust_debit)
            move_dict['line_ids'] = line_ids
            move = self.env['account.move'].create(move_dict)
            slip.write({'move_id': move.id, 'date': date,'state': 'done'})
            move.action_post()
        return True


class HrContract(models.Model):
    _inherit = 'hr.contract'
    _description = 'Employee Contract'

    # override the currency_id and set (original attribute) readonly to False and related to False
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,readonly=False,related=False,
                                  default=lambda self: self.env.user.company_id.currency_id)


