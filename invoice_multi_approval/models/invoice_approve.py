from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class InvoiceApprove(models.Model):
    _inherit = 'account.move'

    def _selection_state(self):
        return [
            ('draft', 'Draft'),
            ('finance_approval', 'Finance Approval'),
            ('md_approval', 'Managing Director Approval'),
            ('posted', 'Posted'),
            ('rejected', 'Rejected'),
        ]

    state = fields.Selection(
        selection=_selection_state,
        string="Status",
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        default='draft'
    )

    def _get_approval_group(self, group_name):
        group = self.env['res.groups'].search([('name', '=', group_name)], limit=1)
        if not group:
            _logger.warning(f"Approval group '{group_name}' not found. Make sure the groups are correctly created.")
        return group

    def action_invoice_approve(self):
        """Submit for approval and move through the stages."""
        for move in self:
            user = self.env.user
            if move.state == 'draft':
                finance_group = self._get_approval_group('Finance Approver')
                if finance_group not in user.groups_id:
                    raise UserError(_("You don't have permission to submit invoices for Finance Approval."))
                move.write({'state': 'finance_approval'})

            elif move.state == 'finance_approval':
                finance_group = self._get_approval_group('Finance Approver')
                if finance_group not in user.groups_id:
                    raise UserError(_("You don't have permission to approve at the Finance stage."))
                move.write({'state': 'md_approval'})

            elif move.state == 'md_approval':
                md_group = self._get_approval_group('Managing Director')
                if md_group not in user.groups_id:
                    raise UserError(_("You don't have permission to approve at the MD stage."))

                move.action_post()

            else:
                raise UserError(_("The invoice is already in a final state (Posted or Rejected)."))

    def action_post(self):
        """Override action_post to allow posting from md_approval."""
        for move in self:
            _logger.info(f"Attempting to post invoice {move.name} with state: {move.state}")

            if move.state not in ['draft', 'md_approval']:
                raise UserError(
                    _("You can only post invoices that are in Draft or MD Approval state. Current state: %s") % move.state
                )

            super(InvoiceApprove, move).action_post()

            move.write({'state': 'posted'})
    def action_refuse(self):
        """Refuse the invoice and move it back to draft state."""
        for move in self:
            if move.state not in ['finance_approval', 'md_approval']:
                raise UserError(_("You can only refuse the invoice at the approval stages."))
            move.write({'state': 'draft'})
            _logger.info(f"Invoice {move.name} has been refused and sent back to draft.")

