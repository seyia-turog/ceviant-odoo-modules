from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class HrContract(models.Model):
    _inherit = 'hr.contract'

    leave_allocation_ids = fields.One2many(
        'hr.leave.allocation', 'contract_id',
        string="Leave Allocations",
        help="Leave allocations associated with this contract."
    )
