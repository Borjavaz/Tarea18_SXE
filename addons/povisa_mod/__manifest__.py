# -*- coding: utf-8 -*-
{
    'name': "gestion povisa",
    'summary': "Modulo sencillo para el control de enfermos y especialistas",
    'description': """
        Este modulo permite gestionar:
        - Pacientes (datos y sintomas)
        - Medicos (datos y numero de colegiado)
        - Citas (union de ambos con el diagnostico)
    """,
    'author': "Borja",
    'website': "https://www.povisa.es",
    'category': 'hospital',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
