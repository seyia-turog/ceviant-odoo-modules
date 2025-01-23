from odoo import models, fields

class HrLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'

    contract_id = fields.Many2one(
        'hr.contract',
        string="Contract",
        help="The contract associated with this leave allocation."
    )

