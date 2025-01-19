{
    'name': 'payslip_customization',
    'version': '2.0.0',
    'category': 'Employees',
    'summary': 'Payslip Customization',
    'description': 'This module provides a custom API endpoint for handling ledger transactions.',
    'author': 'Ceviant',
    'depends': ['account', 'hr_payroll_community'],
    'data': [
        'data/custom_report.xml',
        'data/payslip_reports.xml',
        'views/payslip_view.xml',

    ],
    'installable': True,
    'application': False,
}
