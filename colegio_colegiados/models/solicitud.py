from odoo import models, fields

class SolicitudColegiacion(models.Model):
    _name = 'colegio.solicitud'
    _description = 'Solicitud de Colegiación'
    _inherit = ['mail.thread']

    dni = fields.Char(string='DNI', required=True)
    nombres = fields.Char(string='Nombres', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    correo = fields.Char(string='Correo')
    telefono = fields.Char(string='Teléfono')
    fecha_solicitud = fields.Date(string='Fecha de solicitud', default=fields.Date.context_today)
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En revisión'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ], string='Estado', default='pendiente', tracking=True)
    observaciones = fields.Text(string='Observaciones')
    documento_ids = fields.One2many('colegio.documento', 'solicitud_id', string='Documentos')