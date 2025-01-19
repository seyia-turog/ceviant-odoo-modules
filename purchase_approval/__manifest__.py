{
    'name': 'purchase_approval',
    'version': '1.0.0',
    'summary': 'Adds a custom two-level approval workflow for purchase orders.',
    'description': 'This module introduces a custom workflow for purchase orders with approvals by a line manager and internal control.',
    'author': 'Ceviant',
    'license': 'AGPL-3',
    'depends': ['purchase'],
    'data': [
        # 'data/approval_groups.xml',
        'views/purchase_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
