{
    'name': 'Ledger Sync',
    'version': '2.0.0',
    'category': 'Accounting',
    'summary': 'For handling ledger sync transactions',
    'description': 'This module provides a custom API endpoint for handling ledger transactions.',
    'author': 'TUROG Technologies',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/custom_journal_entry_views.xml',
        'data/cron_jobs.xml',
    ],
    'installable': True,
    'application': False,
}
