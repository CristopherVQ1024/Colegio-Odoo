from odoo import models, fields, api
from datetime import date

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
    cuota_ids = fields.One2many('colegio.cuota', 'colegiado_id', string='Cuotas')

    habilitado = fields.Boolean(string='Habilitado', compute='_compute_habilitado', store=True)

    @api.depends('cuota_ids.estado', 'estado')
    def _compute_habilitado(self):
        for rec in self:
            if rec.estado != 'activo':
                rec.habilitado = False
                continue
            cuotas_vencidas = rec.cuota_ids.filtered(lambda c: c.estado == 'vencido')
            rec.habilitado = not bool(cuotas_vencidas)