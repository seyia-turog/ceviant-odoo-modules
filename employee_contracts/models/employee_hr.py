from odoo import models, api, exceptions, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def write(self, vals):
        restricted_fields = {'expense_manager_id', 'leave_manager_id', 'attendance_manager_id'}

        if restricted_fields.intersection(vals.keys()):

            is_approver = (
                    self.env.user.has_group('expenses.group_expense_all_approver') or
                    self.env.user.has_group('expenses.group_expense_administrator')
            )
            if not is_approver:
                raise exceptions.AccessError(
                    _("You do not have the access rights to modify the approvers for Expense, Time Off, or Attendance.")
                )

        return super(HrEmployee, self).write(vals)
