{
    'name': 'Gestión de Colegiados',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Registro y gestión de colegiados',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/colegiado_views.xml',
    ],
    'installable': True,
    'application': True,
}