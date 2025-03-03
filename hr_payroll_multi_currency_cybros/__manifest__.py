#-*- coding:utf-8 -*-
{
    'name': "HR Payroll Accounting Multi Currency Worked with Cybrosys",

    'summary': """
        HR Payroll Accounting Multi Currency
        """,

    'description': """
Payslip
Payroll
HR Payroll
HR payslip
payroll multi
HR Payroll Accounting
HR Payroll Accounting Multi Currency
HR Payroll journal Entry
HR Payroll account
Payroll Multi Currency
Payslip Currency
Payroll Currency
Payroll Multiple Currency
Payroll account multi currency
payroll accounting
Payslip Multi currency
Payslip account multi currency
Payslip Multiple Currency
Payslip journal entry
Payslip currency
HR Payslip multi currency
multi currency
Salary multi currency
Salary currency
Salary
    """,

    'author': "CorTex IT Solutions Ltd.",
    'website': "https://cortexsolutions.net",
    'support': 'support@cortexsolutions.net',
    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Human Resources',
    'version': '1.0.0',
    'license': 'OPL-1',
    'currency': 'EUR',
    'price': 70,
    # any module necessary for this one to work correctly
    'depends': ['hr_payroll_community','hr_payroll_account_community'],
    # always loaded
    'data': [
             'views/hr_payroll_account_views.xml',
             'views/report_payslip_templates.xml',
             'views/report_payslipdetails_templates.xml'
            ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}