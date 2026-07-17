# -*- coding: utf-8 -*-
{
    'name': 'Tombo City - Gestión Policial Municipal',
    'version': '17.0.1.0.0',
    'category': 'Public Safety',
    'summary': 'Gestión de denuncias, objetos perdidos, permisos de eventos, '
               'incidencias ciudadanas, comisarías y recursos policiales.',
    'description': """
Tombo City
==========
Sistema integral para la gestión de una institución policial municipal:

1. Gestión de Denuncias (núcleo)
2. Gestión de Objetos Perdidos
3. Gestión de Permisos para Eventos
4. Gestión de Incidencias Ciudadanas
5. Gestión de Comisarías (Administración) y Personal Policial
6. Gestión de Recursos Policiales

Incluye 4 roles: Administrador, Personal de Comisaría,
Comisario/Supervisor y Ciudadano (portal).
""",
    'author': 'Cristopher',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'portal', 'web'],
    'data': [
        # Security
        'security/tombo_security_groups.xml',
        'security/tombo_security_rules.xml',
        'security/ir.model.access.csv',
        # Data
        'data/ir_sequence_data.xml',
        # Views - backend
        'views/tombo_comisaria_views.xml',
        'views/tombo_policia_views.xml',
        'views/tombo_recurso_views.xml',
        'views/tombo_denuncia_views.xml',
        'views/tombo_objeto_perdido_views.xml',
        'views/tombo_permiso_evento_views.xml',
        'views/tombo_incidencia_views.xml',
        'views/menu_views.xml',
        # Portal
        'views/portal/portal_templates.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
