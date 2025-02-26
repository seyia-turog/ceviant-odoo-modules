{
    'name': 'Expense Approval',
    'version': '1.0.0',
    'category': 'Human Resources',
    'sequence': 35,
    'summary': 'Expense Approval Process',
    'description': 'Expense Approval Process',
    'depends': ['hr_expense'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/hr_expense_security.xml',
         'data/expense_approval_groups.xml',
    ],
    'installable': True,
    'auto_install': False,
}