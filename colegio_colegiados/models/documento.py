from odoo import models, fields

class Documento(models.Model):
    _name = 'colegio.documento'
    _description = 'Documento de Solicitud'

    tipo_documento = fields.Char(string='Tipo de documento')
    archivo = fields.Binary(string='Archivo')
    archivo_nombre = fields.Char(string='Nombre del archivo')
    fecha_subida = fields.Date(string='Fecha de subida', default=fields.Date.context_today)
    solicitud_id = fields.Many2one('colegio.solicitud', string='Solicitud', ondelete='cascade')