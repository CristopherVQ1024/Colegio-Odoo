from odoo import models, fields

class Colegiado(models.Model):
    _name = 'colegio.colegiado'
    _description = 'Colegiado'
    _inherit = ['mail.thread']

    numero_colegiatura = fields.Char(string='N° de colegiatura', required=True)
    dni = fields.Char(string='DNI')
    nombres = fields.Char(string='Nombres', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    fecha_nacimiento = fields.Date(string='Fecha de nacimiento')
    direccion = fields.Char(string='Dirección')
    telefono = fields.Char(string='Teléfono')
    correo = fields.Char(string='Correo')
    fecha_colegiacion = fields.Date(string='Fecha de colegiación')
    estado = fields.Selection([
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('suspendido', 'Suspendido'),
    ], string='Estado', default='activo', tracking=True)
    especialidad_id = fields.Many2one('colegio.especialidad', string='Especialidad')
    user_id = fields.Many2one('res.users', string='Usuario vinculado')