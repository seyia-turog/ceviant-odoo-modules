from odoo import fields, models, api

class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    bank_name = fields.Char(
        string="Bank Name",
        store=True
    )
    staff_id = fields.Char(
        string="Staff ID",
        related="employee_id.barcode"
    )
    acc_number = fields.Char(string="Account Number", store=True)

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        """
        Populate the bank_name field from the employee when the employee_id is set.
        """
        for payslip in self:
            if payslip.employee_id:
                payslip.bank_name = payslip.employee_id.bank_name
