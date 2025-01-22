{
    'name': 'custom_journal_entry',
    'version': '2.0.0',
    'category': 'Accounting',
    'summary': 'For handling ledger transactions',
    'description': 'This module provides a custom API endpoint for handling ledger transactions.',
    'author': 'Ceviant',
    'depends': ['account', 'hr_payroll_community'],
    'data': [
        'security/ir.model.access.csv',
        # 'data/custom_report.xml',
        # 'data/payslip_reports.xml',
        # 'views/payslip_view.xml',
        'data/cron_jobs.xml',
    ],
    'installable': True,
    'application': False,
}
