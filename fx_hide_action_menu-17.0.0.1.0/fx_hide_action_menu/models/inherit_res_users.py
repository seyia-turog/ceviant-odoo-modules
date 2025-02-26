import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class InheritResUsers(models.Model):
    _inherit = "res.users"

    is_hide_action = fields.Boolean(string="Hide Action All")
    applied_action_models_ids = fields.Many2many(
        comodel_name="ir.model", string="Applied Models for Hiding Action"
    )

    @api.model
    def get_is_hide_action_and_applied_models(self):
        current_user = self.env.user

        is_hide_action = current_user.is_hide_action
        applied_action_models = []
        for model in current_user.applied_action_models_ids:
            applied_action_models.append((model.id, model.model if model else False))

        return {
            "is_hide_action": is_hide_action,
            "applied_action_models_ids": applied_action_models,
        }
