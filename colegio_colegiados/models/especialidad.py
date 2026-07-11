from odoo import models, fields

class Especialidad(models.Model):
    _name = 'colegio.especialidad'
    _description = 'Especialidad'

    name = fields.Char(string='Nombre', required=True)
    descripcion = fields.Text(string='Descripción')