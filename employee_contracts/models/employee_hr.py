from odoo import models, api, exceptions, _
import logging

_logger = logging.getLogger(__name__)

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _get_approval_group(self, group_name):
        """Helper to fetch approval groups by name."""
        group = self.env['res.groups'].search([('name', '=', group_name)], limit=1)
        if not group:
            _logger.warning(f"Approval group '{group_name}' not found. Make sure the groups are correctly created.")
        else:
            _logger.info(f"Approval group '{group_name}' found with ID {group.id}.")
        return group

    @api.model
    def write(self, vals):
        restricted_fields = {'expense_manager_id', 'leave_manager_id', 'attendance_manager_id'}

        approver_group = self._get_approval_group('All Approver')
        admin_group = self._get_approval_group('Administrator')

        _logger.info(f"User: {self.env.user.name} (ID: {self.env.user.id})")
        _logger.info(f"Approver Group: {approver_group.name if approver_group else 'Not Found'}")
        _logger.info(f"Admin Group: {admin_group.name if admin_group else 'Not Found'}")
        _logger.info(f"User in Approver Group: {self.env.user in approver_group.users if approver_group else 'Group Not Found'}")
        _logger.info(f"User in Admin Group: {self.env.user in admin_group.users if admin_group else 'Group Not Found'}")

        if restricted_fields.intersection(vals.keys()):
            is_approver = (
                    (approver_group and self.env.user in approver_group.users) or
                    (admin_group and self.env.user in admin_group.users)
            )
            if not is_approver:
                raise exceptions.AccessError(
                    _("You do not have the access rights to modify the approvers for Expense, Time Off, or Attendance.")
                )

        return super(HrEmployee, self).write(vals)
