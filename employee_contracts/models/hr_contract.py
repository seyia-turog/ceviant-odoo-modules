from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class HrContract(models.Model):
    _inherit = 'hr.contract'

    # Leave Allocation related to the contract
    leave_allocation_ids = fields.One2many(
        'hr.leave.allocation', 'contract_id', string="Leave Allocations",
        help="Leave allocations associated with this contract."
    )

    # Adding probation start and end date fields
    probation_start_date = fields.Date(string='Probation Start Date')
    probation_end_date = fields.Date(string='Probation End Date')

    # Modifying the contract state to include "On Probation" and "Confirmed"
    state = fields.Selection(
        [('draft', 'On Probation'), ('open', 'Confirmed'),
         ('close', 'Expired'), ('cancel', 'Cancelled')],
        string='Contract Status', readonly=True, default='draft',
        tracking=True,
    )

    # Adding a button to approve and move the employee from probation to confirmed
    def action_approve(self):
        for contract in self:
            # Ensure only Line Managers can approve
            if not self.env.user.has_group('hr.group_hr_manager'):
                raise UserError("Only Line Managers can approve this action.")

            # Check probation end date for validation
            if contract.state == 'draft':
                if not contract.probation_end_date or contract.probation_end_date > fields.Date.today():
                    raise UserError("Probation period must be completed before approval.")
                contract.state = 'open'
            elif contract.state == 'open':
                contract.state = 'close'
            elif contract.state == 'close':
                contract.state = 'cancel'
            else:
                raise UserError("Approval is not allowed in the current state.")

    @api.model
    def create(self, values):
        if 'state' not in values:
            values['state'] = 'draft'
        return super(HrContract, self).create(values)
