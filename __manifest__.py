{
    'name': 'LC Management System',
    'version': '18.1.0',
    'summary': 'Manage Letter of Credit ',
    'description': """
        Manage LC Requests: Draft → Approved → Closed
        Attach documents and link with Purchase Orders
    """,
    'category': 'Finance',
    'author': 'Muntasir Kamal',
    'depends': ['base','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/lc_management_views.xml',
    ],
    'installable': True,
    'application': True,
}