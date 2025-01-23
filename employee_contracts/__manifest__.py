{
    'name': 'employee_contracts',
    'version': '2.0.0',
    'summary': '',
    'description': '',
    'author': 'Ceviant',
    'depends': ['hr_contract', 'hr_holidays', 'hr', 'purchase', 'base'],
    'data': [
        'views/hr_contract_view.xml',
        'views/hr_employee_view.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
