from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('line_manager', 'Line Manager Approval'),
        ('internal_control', 'Internal Control Approval'),
        ('managing_director', 'Managing Director Approval'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], default='draft')

    def _get_approval_group(self, group_name):
        """Helper to fetch approval groups by name."""
        group = self.env['res.groups'].search([('name', '=', group_name)], limit=1)
        if not group:
            _logger.warning(f"Approval group '{group_name}' not found. Make sure the groups are correctly created.")
        return group

    def action_submit_for_approval(self):
        """Submit the RFQ for Line Manager approval."""
        for order in self:
            if order.state != 'draft':
                raise UserError(_("Order is already submitted for approval."))
            order.write({'state': 'line_manager'})

    def action_approve(self):
        """Approve the order based on the current stage and user group."""
        for order in self:
            user = self.env.user
            line_manager_group = self._get_approval_group('Line Manager')
            internal_control_group = self._get_approval_group('Internal Control')
            managing_director_group = self._get_approval_group('Managing Director')

            if order.state == 'line_manager':
                if line_manager_group not in user.groups_id:
                    raise UserError(_("You don't have the permission to approve at the Line Manager stage."))
                order.write({'state': 'internal_control'})
            elif order.state == 'internal_control':
                if internal_control_group not in user.groups_id:
                    raise UserError(_("You don't have the permission to approve at the Internal Control stage."))
                order.write({'state': 'managing_director'})
            elif order.state == 'managing_director':
                if managing_director_group not in user.groups_id:
                    raise UserError(_("You don't have the permission to approve at the Managing Director stage."))
                order.write({'state': 'purchase'})
                order.button_confirm()
            else:
                raise UserError(_("Approval is not allowed in the current state."))

    def action_refuse(self):
        """Refuse the order and send it back to the originator (draft state)."""
        for order in self:
            if order.state not in ['line_manager', 'internal_control', 'managing_director']:
                raise UserError(_("You can only refuse an order at the approval stages."))
            order.write({'state': 'draft'})
            _logger.info(f"Order {order.name} has been refused and sent back to draft.")
