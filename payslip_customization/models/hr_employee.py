from odoo import fields, models

class Employee(models.Model):
    _inherit = "hr.employee"


    acc_number = fields.Char(related='bank_account_id.acc_number', string='Bank Account Number')
    bank_name = fields.Char(related='bank_account_id.bank_id.name', string='Bank Name')

