from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    subtotal = fields.Monetary(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('price_unit', 'product_qty')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.price_unit * line.product_qty
