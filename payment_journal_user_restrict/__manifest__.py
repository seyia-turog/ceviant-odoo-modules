
{
    'name': 'Payment Journal Confirmation User Restrict',
    'version': '7.0.1',
    'category': 'Accounting',
    "author": 'Zero Systems',
    "company": 'Zero for Information Systems',
    "website": "https://www.erpzero.com",
    "email": "sales@erpzero.com",
    "sequence": 0,
    'license': 'OPL-1',
    'live_test_url': 'https://youtu.be/j6LDUhpYemI',
    'summary': """Payments Internal Transfers Confirmation User Restrict""",
    'description': """
        Confirmation of the Payments Internal Transfers is the right of the user who has rights on the Paymant Journal transferred to him only """,
    'depends': ['base','account'],
    'data': [
        'views/view.xml',
    ],
    'images': ['static/description/payment_transfers.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
    'pre_init_check': 'pre_init_check',
    "price": 00.0,
    "currency": 'EUR',
}
