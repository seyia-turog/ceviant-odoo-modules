from odoo import models, fields, api


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    original_rate = fields.Float(
        string='Tipo de cambio',
        readonly=True,
        compute='_compute_original_rate',
        store=True,
        help="Original currency exchange rate on the payslip date."
    )

    @api.depends('company_id.currency_id', 'currency_id')
    def _compute_original_rate(self):
        for record in self:
            if record.company_id and record.currency_id:
                # Use today's date instead of date_to
                today = fields.Date.today()

                # Search for matching currency rate record based on today's date
                currency_rate = self.env['res.currency.rate'].search([
                    ('name', '=', today),  # Search for today's rate
                    ('company_id', '=', record.company_id.id),
                    ('currency_id', '=', record.currency_id.id),
                    # ('state', '=', 'confirmed'),  # Optional: Filter by confirmed rates
                ], limit=1)
                if currency_rate:
                    # Use the first matching rate (assuming rates are ordered by date)
                    record.original_rate = currency_rate[0].original_rate
                else:
                    record.original_rate = 0
            else:
                record.original_rate = 0

    def action_payslip_done(self):
        # Override the original action_payslip_done method
        super(HrPayslip, self).action_payslip_done()
        # Ensure the original_rate is recomputed on confirmation
        self._compute_original_rate()
